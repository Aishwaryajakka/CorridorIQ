#!/usr/bin/env python3
"""Build the reproducible CorridorIQ hackathon MVP dataset from local inputs."""

from pathlib import Path

import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

RAW = Path("data/raw")
TRACTS = RAW / "boundaries/texas_tracts/tl_2024_48_tract/tl_2024_48_tract.shp"
POPULATION = RAW / "census/B01003/ACSDT5Y2024.B01003-Data.csv"
INCOME = RAW / "census/B19013/ACSDT5Y2024.B19013-Data.csv"
VEHICLES = RAW / "census/B08201/ACSDT5Y2024.B08201-Data.csv"
STOPS = RAW / "metro/stops.txt"
LANDUSE = RAW / "landuse/hgac_current_landuse.geojson"
OUT = Path("data/processed")
CSV_OUT = OUT / "corridoriq_tracts.csv"
GEOJSON_OUT = OUT / "corridoriq_tracts.geojson"

SQ_METERS_PER_SQ_MILE = 2_589_988.110336
METERS_PER_MILE = 1_609.344
NRG_LAT, NRG_LON = 29.6847, -95.4107
FIFA_RADIUS_MILES = 20.0

# Single source of truth for the prototype's analytical logic. These formulas
# are intentionally transparent diagnostics, not fitted or predictive models.
METHODOLOGY = {
    "economic_score": "Robust 0-100 min-max normalization of median household income.",
    "activity_score": "Robust 0-100 min-max normalization of population per land square mile.",
    "mobility_score": "70% normalized transit stops per square mile + 30% inverse normalized no-vehicle household share.",
    "mismatch_score": "Normalize max(activity_score - mobility_score, 0) to 0-100 using the same robust min-max method.",
    "fifa_relevance": "70% NRG proximity (linear from 100 at NRG to 0 at 20 miles) + 30% transit_supply_score.",
    "legacy_priority": "mismatch_score * fifa_relevance / 100.",
}


def log(message=""):
    print(message, flush=True)


def read_acs(path, fields):
    """Read only ACS tract records; the second CSV row contains labels."""
    frame = pd.read_csv(path, skiprows=[1], dtype={"GEO_ID": "string"}, low_memory=False)
    frame = frame[frame["GEO_ID"].str.startswith("1400000US", na=False)].copy()
    frame["GEOID"] = frame["GEO_ID"].str.replace("1400000US", "", regex=False)
    if not frame["GEOID"].str.fullmatch(r"\d{11}").all():
        raise ValueError(f"Invalid tract GEOID encountered in {path}")
    result = frame[["GEOID", *fields]].copy()
    for field in fields:
        if field != "NAME":
            result[field] = pd.to_numeric(result[field], errors="coerce")
            result.loc[result[field] < 0, field] = pd.NA  # ACS missing-value sentinels
    return result


def robust_minmax(series, lower_quantile=0.02, upper_quantile=0.98):
    """Return 0-100 min-max scores after clipping observed tails; keep NaNs."""
    values = pd.to_numeric(series, errors="coerce")
    observed = values.dropna()
    result = pd.Series(float("nan"), index=series.index, dtype=float)
    if observed.empty:
        return result
    low, high = observed.quantile([lower_quantile, upper_quantile])
    if high <= low:
        result.loc[values.notna()] = 50.0
        return result
    result.loc[values.notna()] = ((values.clip(low, high) - low) / (high - low) * 100).loc[values.notna()]
    return result


def priority_reason(row):
    if pd.isna(row["legacy_priority"]):
        return "Insufficient source data to calculate a complete priority score."
    if row["corridor_type"] == "High-Intensity / Mobility Gap":
        return "High population density and mobility mismatch, combined with strong FIFA relevance."
    if row["corridor_type"] == "Established Urban Hub":
        return "High urban activity with comparatively balanced mobility capacity."
    if row["corridor_type"] == "Emerging Opportunity":
        return "Moderate urban intensity and mobility mismatch with timely FIFA proximity."
    return "Lower mismatch and/or FIFA relevance relative to other Harris County tracts."


def main():
    log("CorridorIQ data preparation")
    required = [TRACTS, POPULATION, INCOME, VEHICLES]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required local inputs: " + ", ".join(missing))
    if not LANDUSE.exists() or LANDUSE.stat().st_size <= 100:
        log("WARNING: H-GAC land use is unavailable/empty; continuing without it.")
    else:
        log("Optional local H-GAC land use found; MVP scoring remains tract-proxy based.")
    log("No remote land-use download will be attempted.")

    tracts = gpd.read_file(TRACTS)
    gdf = tracts[(tracts["STATEFP"] == "48") & (tracts["COUNTYFP"] == "201")].copy()
    gdf["GEOID"] = gdf["GEOID"].astype("string").str.zfill(11)
    if len(gdf) != gdf["GEOID"].nunique() or not gdf["GEOID"].str.fullmatch(r"\d{11}").all():
        raise ValueError("Harris tract GEOIDs are not unique 11-digit strings")

    population = read_acs(POPULATION, ["NAME", "B01003_001E"]).rename(
        columns={"NAME": "tract_name", "B01003_001E": "population"})
    income = read_acs(INCOME, ["B19013_001E"]).rename(columns={"B19013_001E": "median_income"})
    vehicles = read_acs(VEHICLES, ["B08201_001E", "B08201_002E"]).rename(
        columns={"B08201_001E": "households", "B08201_002E": "no_vehicle_households"})
    vehicles["no_vehicle_pct"] = (
        vehicles["no_vehicle_households"] / vehicles["households"].replace(0, pd.NA) * 100
    )
    gdf = gdf.merge(population, on="GEOID", how="left", validate="one_to_one")
    gdf = gdf.merge(income, on="GEOID", how="left", validate="one_to_one")
    gdf = gdf.merge(vehicles, on="GEOID", how="left", validate="one_to_one")
    gdf["land_sq_miles"] = pd.to_numeric(gdf["ALAND"], errors="coerce") / SQ_METERS_PER_SQ_MILE
    gdf["population_density"] = gdf["population"] / gdf["land_sq_miles"].replace(0, pd.NA)
    gdf = gdf.to_crs(4326)

    # Local GTFS is useful but optional. Zero assigned stops is an observed count,
    # not an imputation. If GTFS is absent, mobility uses need alone as documented.
    transit_available = STOPS.exists()
    if transit_available:
        stops = pd.read_csv(STOPS, low_memory=False)
        stops["stop_lat"] = pd.to_numeric(stops["stop_lat"], errors="coerce")
        stops["stop_lon"] = pd.to_numeric(stops["stop_lon"], errors="coerce")
        stops = stops.dropna(subset=["stop_lat", "stop_lon"])
        stop_points = gpd.GeoDataFrame(stops, geometry=gpd.points_from_xy(stops.stop_lon, stops.stop_lat), crs=4326)
        joined = gpd.sjoin(stop_points, gdf[["GEOID", "geometry"]], how="inner", predicate="within")
        counts = joined.groupby("GEOID").size().rename("transit_stops")
        gdf = gdf.merge(counts, on="GEOID", how="left")
        gdf["transit_stops"] = gdf["transit_stops"].fillna(0).astype(int)
        gdf["transit_stops_per_sq_mile"] = gdf["transit_stops"] / gdf["land_sq_miles"].replace(0, pd.NA)
    else:
        log("WARNING: local transit stops absent; using mobility need alone.")
        gdf["transit_stops"] = pd.NA
        gdf["transit_stops_per_sq_mile"] = pd.NA

    gdf["economic_score"] = robust_minmax(gdf["median_income"])
    gdf["activity_score"] = robust_minmax(gdf["population_density"])
    gdf["mobility_need_score"] = robust_minmax(gdf["no_vehicle_pct"])
    if transit_available:
        gdf["transit_supply_score"] = robust_minmax(gdf["transit_stops_per_sq_mile"])
        # Higher mobility capacity means more transit supply and less unmet need.
        gdf["mobility_score"] = 0.70 * gdf["transit_supply_score"] + 0.30 * (100 - gdf["mobility_need_score"])
    else:
        gdf["transit_supply_score"] = pd.NA
        gdf["mobility_score"] = 100 - gdf["mobility_need_score"]

    gdf["mismatch_raw"] = gdf["activity_score"] - gdf["mobility_score"]
    gdf["mismatch_severity_raw"] = gdf["mismatch_raw"].clip(lower=0)
    gdf["mismatch_score"] = robust_minmax(gdf["mismatch_severity_raw"])

    projected = gdf.to_crs(32615)
    projected_centroids = projected.geometry.centroid
    nrg = gpd.GeoSeries([Point(NRG_LON, NRG_LAT)], crs=4326).to_crs(32615).iloc[0]
    gdf["distance_to_nrg_miles"] = projected_centroids.distance(nrg).values / METERS_PER_MILE
    gdf["nrg_proximity_score"] = (100 * (1 - gdf["distance_to_nrg_miles"] / FIFA_RADIUS_MILES)).clip(0, 100)
    gdf["fifa_relevance"] = (0.70 * gdf["nrg_proximity_score"] + 0.30 * gdf["transit_supply_score"]
                              if transit_available else gdf["nrg_proximity_score"])
    gdf["legacy_priority"] = gdf["mismatch_score"] * gdf["fifa_relevance"] / 100

    activity_q75 = gdf["activity_score"].quantile(0.75)
    positive_mismatch_median = gdf.loc[gdf["mismatch_score"] > 0, "mismatch_score"].median()
    fifa_median = gdf["fifa_relevance"].median()
    def classify(row):
        if pd.isna(row["legacy_priority"]): return "Insufficient Data"
        if row["activity_score"] >= activity_q75 and row["mismatch_score"] >= positive_mismatch_median:
            return "High-Intensity / Mobility Gap"
        if row["activity_score"] >= activity_q75 and row["mismatch_score"] < positive_mismatch_median:
            return "Established Urban Hub"
        if (row["activity_score"] >= gdf["activity_score"].median()
                and row["mismatch_score"] > 0 and row["fifa_relevance"] >= fifa_median):
            return "Emerging Opportunity"
        return "Lower Priority"
    gdf["corridor_type"] = gdf.apply(classify, axis=1)
    gdf["priority_reason"] = gdf.apply(priority_reason, axis=1)

    centroids = gpd.GeoSeries(projected_centroids, crs=32615).to_crs(4326)
    gdf["latitude"], gdf["longitude"] = centroids.y.values, centroids.x.values
    columns = ["GEOID", "tract_name", "latitude", "longitude", "population", "land_sq_miles",
        "population_density", "median_income", "households", "no_vehicle_households", "no_vehicle_pct",
        "transit_stops", "transit_stops_per_sq_mile", "economic_score", "activity_score",
        "mobility_need_score", "transit_supply_score", "mobility_score", "mismatch_raw",
        "mismatch_severity_raw", "mismatch_score", "distance_to_nrg_miles", "nrg_proximity_score",
        "fifa_relevance", "legacy_priority", "corridor_type", "priority_reason"]
    OUT.mkdir(parents=True, exist_ok=True)
    gdf[columns].to_csv(CSV_OUT, index=False)
    gdf[[*columns, "geometry"]].to_file(GEOJSON_OUT, driver="GeoJSON", index=False)

    log("\nQA SUMMARY")
    log(f"Harris County tracts: {len(gdf):,}")
    for label, column in [("Population", "population"), ("Income", "median_income"),
                          ("Vehicle", "no_vehicle_pct"), ("Density", "population_density")]:
        log(f"{label} non-null: {gdf[column].notna().sum():,}")
    for column in ["population", "median_income", "no_vehicle_pct", "population_density"]:
        values = gdf[column].dropna()
        log(f"{column}: min={values.min():,.2f}, median={values.median():,.2f}, max={values.max():,.2f}")
    log(f"legacy_priority: median={gdf['legacy_priority'].median():.2f}, max={gdf['legacy_priority'].max():.2f}")
    log(f"mismatch_score: median={gdf['mismatch_score'].median():.2f}, max={gdf['mismatch_score'].max():.2f}")
    log("\nTOP 10 LEGACY PRIORITIES")
    log(gdf.nlargest(10, "legacy_priority")[["GEOID", "tract_name", "corridor_type", "mismatch_score",
        "fifa_relevance", "legacy_priority"]].to_string(index=False))
    log(f"\nSaved {CSV_OUT}\nSaved {GEOJSON_OUT}")


if __name__ == "__main__":
    main()
