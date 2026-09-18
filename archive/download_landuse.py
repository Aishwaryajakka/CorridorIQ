#!/usr/bin/env python3
"""Robustly download H-GAC land-use polygons intersecting Harris County."""

from __future__ import annotations

import json
import os
import random
import sys
import time
from pathlib import Path

import geopandas as gpd
import pandas as pd
import requests
from shapely.geometry import GeometryCollection, Polygon, box, shape

LAYER = "https://gis.h-gac.com/arcgis/rest/services/Land_Use/Current_Land_Use/MapServer/0"
QUERY = LAYER + "/query"
OUTPUT = Path("data/raw/landuse/hgac_current_landuse.geojson")
HARRIS_BOUNDS = (-95.960733, 29.497297, -94.908492, 30.170606)
FIELDS = ["OBJECTID", "ParcelID", "County", "Label_Current_Land_Use", "Acres",
          "RES", "COM", "IND", "MUL", "GME", "OTH", "POS", "VDF", "UND", "UNK"]


class ArcGISError(RuntimeError):
    pass


def log(text):
    print(text, flush=True)


def request_json(session, url, params, method="GET", attempts=5):
    """Make a retrying ArcGIS request and also detect errors returned with HTTP 200."""
    last = None
    for attempt in range(1, attempts + 1):
        try:
            response = (session.post(url, data=params, timeout=(20, 180)) if method == "POST"
                        else session.get(url, params=params, timeout=(20, 180)))
            response.raise_for_status()
            if not response.content:
                raise ArcGISError("empty server response")
            data = response.json()
            if "error" in data:
                error = data["error"]
                raise ArcGISError(
                    f"ArcGIS {error.get('code', '?')}: {error.get('message', error)}; "
                    f"details={error.get('details', [])}"
                )
            return data
        except (requests.RequestException, ValueError, ArcGISError) as exc:
            last = exc
            if attempt < attempts:
                delay = min(20, 1.5 * 2 ** (attempt - 1)) + random.random()
                log(f"  attempt {attempt}/{attempts} failed: {exc}; retrying in {delay:.1f}s")
                time.sleep(delay)
    raise ArcGISError(str(last))


def harris_geometry():
    """Use local Census tracts when present, otherwise the supplied tract extent."""
    for path in sorted(Path("data/raw/boundaries").glob("**/tl_*_48_tract.shp")):
        try:
            tracts = gpd.read_file(path)
            col = next((c for c in ("COUNTYFP", "COUNTYFP20") if c in tracts), None)
            if col:
                # Census FIPS 201 does not imply anything about H-GAC's County field.
                selected = tracts[tracts[col].astype(str).str.zfill(3) == "201"]
                if not selected.empty:
                    geom = selected.to_crs(4326).geometry.union_all()
                    if not geom.is_empty:
                        return geom, f"dissolved local Census tracts ({path})"
        except Exception as exc:
            log(f"  warning: could not use {path}: {exc}")
    return box(*HARRIS_BOUNDS), "provided Harris tract extent (envelope fallback)"


def existing_valid(path, harris):
    try:
        frame = gpd.read_file(path)
        return (not frame.empty and frame.crs is not None and
                box(*frame.to_crs(4326).total_bounds).intersects(harris.envelope))
    except Exception:
        return False


def esri_shape(geometry):
    """Convert Esri JSON. XOR reconstructs polygon holes independent of orientation."""
    if not geometry:
        return None
    if "x" in geometry:
        return shape({"type": "Point", "coordinates": [geometry["x"], geometry["y"]]})
    if "paths" in geometry:
        paths = geometry["paths"]
        return shape({"type": "LineString" if len(paths) == 1 else "MultiLineString",
                      "coordinates": paths[0] if len(paths) == 1 else paths})
    polygons = [Polygon(r) for r in geometry.get("rings", []) if len(r) >= 4]
    polygons = [p for p in polygons if not p.is_empty]
    if not polygons:
        return GeometryCollection()
    result = polygons[0]
    for polygon in polygons[1:]:
        result = result.symmetric_difference(polygon)
    return result


def to_gdf(data):
    features = data.get("features", [])
    if not features:
        return gpd.GeoDataFrame(geometry=[], crs=4326)
    if features[0].get("type") == "Feature":
        return gpd.GeoDataFrame.from_features(features, crs=4326)
    rows = []
    for feature in features:
        row = dict(feature.get("attributes") or {})
        row["geometry"] = esri_shape(feature.get("geometry"))
        rows.append(row)
    return gpd.GeoDataFrame(rows, geometry="geometry", crs=4326)


def query_features(session, params):
    """Prefer advertised GeoJSON, but fall back to Esri JSON conversion."""
    try:
        return to_gdf(request_json(session, QUERY,
                      {**params, "outSR": 4326, "f": "geojson"}, "GET"))
    except ArcGISError as exc:
        log(f"  GeoJSON failed ({exc}); trying f=json")
        return to_gdf(request_json(session, QUERY,
                      {**params, "outSR": 4326, "f": "json"}, "GET"))


def spatial_ids(session, bounds):
    xmin, ymin, xmax, ymax = bounds
    base = {"where": "1=1", "geometryType": "esriGeometryEnvelope", "inSR": 4326,
            "spatialRel": "esriSpatialRelIntersects", "returnIdsOnly": "true",
            "returnGeometry": "false", "f": "json"}
    forms = [json.dumps({"xmin": xmin, "ymin": ymin, "xmax": xmax, "ymax": ymax,
                         "spatialReference": {"wkid": 4326}}, separators=(",", ":")),
             f"{xmin},{ymin},{xmax},{ymax}"]
    errors = []
    for geometry in forms:
        try:
            data = request_json(session, QUERY, {**base, "geometry": geometry}, "GET", 2)
            return sorted({int(value) for value in data.get("objectIds") or []})
        except ArcGISError as exc:
            errors.append(str(exc))
    raise ArcGISError("; ".join(errors))


def spatial_filter(frame, harris):
    if frame.empty:
        return frame
    frame = frame[frame.geometry.notna() & ~frame.geometry.is_empty].copy()
    return frame[frame.geometry.intersects(harris)].copy()


def fetch_ids(session, ids, fields, harris, page_size):
    kept, observed = [], set()
    pages = (len(ids) + page_size - 1) // page_size
    for start in range(0, len(ids), page_size):
        part = ids[start:start + page_size]
        frame = query_features(session, {"objectIds": ",".join(map(str, part)),
            "outFields": ",".join(fields), "returnGeometry": "true"})
        if "County" in frame:
            observed.update(map(str, frame["County"].dropna().unique()))
        selected = spatial_filter(frame, harris)
        if not selected.empty:
            kept.append(selected)
        log(f"  ID page {start // page_size + 1}/{pages}: got {len(frame):,}, kept {len(selected):,}")
    return kept, observed


def scan_oids(session, oid, fields, harris, page_size):
    """Keyset pagination avoids skipped/duplicated rows from unreliable offsets."""
    kept, observed, last_oid, page = [], set(), -1, 0
    while True:
        page += 1
        frame = query_features(session, {"where": f"{oid} > {last_oid}",
            "outFields": ",".join(fields), "returnGeometry": "true",
            "orderByFields": f"{oid} ASC", "resultRecordCount": page_size})
        if frame.empty:
            break
        if oid not in frame:
            raise ArcGISError(f"response omitted required field {oid}")
        new_last = int(pd.to_numeric(frame[oid], errors="raise").max())
        if new_last <= last_oid:
            raise ArcGISError("OBJECTID pagination stopped advancing")
        last_oid = new_last
        if "County" in frame:
            observed.update(map(str, frame["County"].dropna().unique()))
        selected = spatial_filter(frame, harris)
        if not selected.empty:
            kept.append(selected)
        log(f"  scan page {page}: got {len(frame):,}, kept {len(selected):,}, last {oid}={last_oid}")
        if len(frame) < page_size:
            break
    return kept, observed


def main():
    log("H-GAC current land-use downloader")
    harris, source = harris_geometry()
    log(f"Harris boundary: {source}")
    log(f"Harris bounds (EPSG:4326): {[round(v, 6) for v in harris.bounds]}")
    protected = existing_valid(OUTPUT, harris)
    if OUTPUT.exists():
        log(f"Existing output: {'valid (will be preserved on failure)' if protected else 'invalid/empty'}")

    session = requests.Session()
    session.headers["User-Agent"] = "CorridorIQ-landuse-downloader/1.0"
    try:
        metadata = request_json(session, LAYER, {"f": "json"})
        if metadata.get("geometryType") != "esriGeometryPolygon":
            raise ArcGISError(f"expected polygons, got {metadata.get('geometryType')}")
        definitions = {field["name"]: field for field in metadata.get("fields", [])}
        oid = next((f["name"] for f in metadata.get("fields", [])
                    if f.get("type") == "esriFieldTypeOID"), None)
        if not oid:
            raise ArcGISError("layer metadata has no OID field")
        fields = [name for name in FIELDS if name in definitions]
        if oid not in fields:
            fields.insert(0, oid)
        maximum = int(metadata.get("maxRecordCount") or 1000)
        # Keep GET URLs and response bodies modest. This old 10.61 service can
        # advertise a huge maximum yet still time out on large requests.
        page_size = max(1, min(maximum, 500))
        log(f"Service: ArcGIS {metadata.get('currentVersion', '?')}; OID={oid}; "
            f"maxRecordCount={maximum:,}; formats={metadata.get('supportedQueryFormats', '?')}")
        county = definitions.get("County")
        if county:
            log(f"County field: {county.get('type')}, length={county.get('length')}, "
                f"coded domain={'yes' if county.get('domain') else 'no'}")
        missing = [name for name in FIELDS if name not in definitions]
        if missing:
            log("Warning: metadata lacks fields: " + ", ".join(missing))

        try:
            log("Trying spatial returnIdsOnly query (no guessed County code)...")
            ids = spatial_ids(session, harris.bounds)
            if not ids:
                raise ArcGISError("spatial query returned zero IDs")
            log(f"Spatial query found {len(ids):,} candidate OBJECTIDs")
            frames, observed = fetch_ids(session, ids, fields, harris, page_size)
            mode = "spatial OBJECTID chunks"
        except ArcGISError as exc:
            log(f"Spatial-ID query unavailable: {exc}")
            log("Falling back to OBJECTID keyset scan plus local spatial filtering...")
            frames, observed = scan_oids(session, oid, fields, harris, page_size)
            mode = "OBJECTID keyset scan"

        if not frames:
            raise ArcGISError("no Harris-intersecting polygons; refusing to write an empty result")
        result = gpd.GeoDataFrame(pd.concat(frames, ignore_index=True), crs=4326)
        result = result.drop_duplicates(subset=oid).reset_index(drop=True)
        bounds = tuple(map(float, result.total_bounds))
        if result.empty or not box(*bounds).intersects(harris.envelope):
            raise ArcGISError(f"result bounds {bounds} do not overlap Harris County")
        result_values = sorted(map(str, result["County"].dropna().unique())) if "County" in result else []
        log(f"County values observed in spatial result: {result_values or ['<null/absent>']}")
        if len(result_values) == 1:
            log(f"Spatial evidence identifies H-GAC Harris value as {result_values[0]!r}")
        else:
            log("County is mixed/unreliable; using the verified spatial selection")

        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        temp = OUTPUT.with_name(f".{OUTPUT.name}.{os.getpid()}.tmp.geojson")
        try:
            result.to_file(temp, driver="GeoJSON", index=False)
            check = gpd.read_file(temp).to_crs(4326)
            check_bounds = tuple(map(float, check.total_bounds))
            if check.empty or not box(*check_bounds).intersects(harris.envelope):
                raise ArcGISError("temporary GeoJSON failed bounds validation")
            os.replace(temp, OUTPUT)  # Atomic: old valid output survives every earlier failure.
        finally:
            if temp.exists():
                temp.unlink()
        log(f"Complete: {len(result):,} features via {mode}")
        log(f"Bounds (EPSG:4326): {[round(v, 6) for v in bounds]}")
        log(f"Wrote {OUTPUT}")
        return 0
    except Exception as exc:
        log(f"ERROR: {exc}")
        log(f"Preserved existing valid file: {OUTPUT}" if protected else "No output was replaced.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
