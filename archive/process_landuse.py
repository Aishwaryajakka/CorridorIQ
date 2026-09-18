import geopandas as gpd
import pandas as pd
from pathlib import Path


LANDUSE_PATH = Path("data/raw/landuse/hgac_current_landuse.geojson")

if not LANDUSE_PATH.exists() or LANDUSE_PATH.stat().st_size <= 100:
    print("WARNING: No usable local H-GAC land-use file; skipping optional land-use processing.")
    print("The CorridorIQ MVP remains available through prepare_data.py and app.py.")
    raise SystemExit(0)


# =========================================================
# 1. READ H-GAC LAND USE
# =========================================================

landuse = gpd.read_file(
    LANDUSE_PATH
)

if landuse.empty or "Label_Current_Land_Use" not in landuse.columns:
    print("WARNING: H-GAC land-use file is empty or lacks the expected category field; skipping it.")
    raise SystemExit(0)

print("Land-use features:", len(landuse))
print("Land-use CRS:", landuse.crs)
print()
print("Columns:")
print(landuse.columns.tolist())

print()
print("Land-use categories:")
print(
    landuse["Label_Current_Land_Use"]
    .value_counts(dropna=False)
)


# =========================================================
# 2. READ HARRIS COUNTY TRACTS
# =========================================================

tracts = gpd.read_file(
    "data/processed/houston_urban_dna.geojson"
)

print()
print("Tracts loaded:", len(tracts))


# =========================================================
# 3. PROJECT BOTH DATASETS
# =========================================================
# We need a projected CRS so area calculations are meaningful.
# EPSG:32615 = UTM Zone 15N, suitable for Houston.

landuse = landuse.to_crs("EPSG:32615")
tracts = tracts.to_crs("EPSG:32615")


# =========================================================
# 4. KEEP ONLY FIELDS WE NEED
# =========================================================

landuse = landuse[
    [
        "Label_Current_Land_Use",
        "geometry"
    ]
].copy()

tracts_small = tracts[
    [
        "GEOID",
        "geometry"
    ]
].copy()


# =========================================================
# 5. INTERSECT LAND USE WITH CENSUS TRACTS
# =========================================================

print()
print("Intersecting land-use polygons with census tracts...")
print("This may take a few minutes.")

intersection = gpd.overlay(
    landuse,
    tracts_small,
    how="intersection",
    keep_geom_type=False
)

print("Intersection pieces:", len(intersection))


# =========================================================
# 6. CALCULATE INTERSECTION AREA
# =========================================================

intersection["area_sq_m"] = intersection.geometry.area


# =========================================================
# 7. SIMPLIFY LAND-USE CATEGORIES
# =========================================================

category_map = {
    "Residential": "residential",
    "Commercial": "commercial",
    "Industrial": "industrial",
    "Parks/Open Spaces": "parks_open_space",
    "Vacant Developable (includes Farming)": "vacant_developable",
    "Gov/Med/Edu": "institutional",
    "Multiple": "mixed",
    "Other": "other",
    "Undevelopable": "undevelopable",
    "Unknown": "unknown",
    "Undetermined": "unknown"
}

intersection["landuse_group"] = (
    intersection["Label_Current_Land_Use"]
    .map(category_map)
    .fillna("other")
)


# =========================================================
# 8. SUM AREA BY TRACT AND LAND-USE TYPE
# =========================================================

summary = (
    intersection
    .groupby(
        [
            "GEOID",
            "landuse_group"
        ]
    )["area_sq_m"]
    .sum()
    .reset_index()
)


# =========================================================
# 9. PIVOT TO ONE ROW PER TRACT
# =========================================================

pivot = summary.pivot(
    index="GEOID",
    columns="landuse_group",
    values="area_sq_m"
).fillna(0)

pivot = pivot.reset_index()


# =========================================================
# 10. MAKE SURE EXPECTED COLUMNS EXIST
# =========================================================

expected = [
    "residential",
    "commercial",
    "industrial",
    "parks_open_space",
    "vacant_developable",
    "institutional",
    "mixed",
    "other",
    "undevelopable",
    "unknown"
]

for col in expected:
    if col not in pivot.columns:
        pivot[col] = 0


# =========================================================
# 11. CALCULATE TOTAL MAPPED LAND-USE AREA
# =========================================================

pivot["mapped_area_sq_m"] = pivot[
    expected
].sum(axis=1)


# =========================================================
# 12. CALCULATE LAND-USE PERCENTAGES
# =========================================================

for col in expected:
    pivot[f"{col}_pct"] = (
        pivot[col]
        / pivot["mapped_area_sq_m"].replace(0, pd.NA)
        * 100
    )


# =========================================================
# 13. CREATE SIMPLE LAND-USE SCORES
# =========================================================

def percentile_score(series):
    return series.rank(
        pct=True,
        method="average"
    ) * 100


# Commercial intensity
pivot["commercial_score"] = percentile_score(
    pivot["commercial_pct"]
)

# Developable land opportunity
pivot["vacant_score"] = percentile_score(
    pivot["vacant_developable_pct"]
)

# Mixed-use signal:
# combine explicitly mixed parcels with residential/commercial coexistence
pivot["res_com_balance"] = (
    100
    - (
        pivot["residential_pct"]
        - pivot["commercial_pct"]
    ).abs()
).clip(lower=0)

pivot["landuse_mix_raw"] = (
    pivot["mixed_pct"] * 0.40
    + pivot["res_com_balance"] * 0.60
)

pivot["landuse_mix_score"] = percentile_score(
    pivot["landuse_mix_raw"]
)


# =========================================================
# 14. CREATE DEVELOPMENT POTENTIAL SCORE
# =========================================================
# Prototype interpretation:
# vacant/developable land + commercial presence + mixed-use potential

pivot["development_potential_score"] = (
    pivot["vacant_score"] * 0.50
    + pivot["commercial_score"] * 0.20
    + pivot["landuse_mix_score"] * 0.30
)


# =========================================================
# 15. KEEP FINAL LAND-USE FIELDS
# =========================================================

landuse_final = pivot[
    [
        "GEOID",
        "residential_pct",
        "commercial_pct",
        "industrial_pct",
        "parks_open_space_pct",
        "vacant_developable_pct",
        "institutional_pct",
        "mixed_pct",
        "commercial_score",
        "landuse_mix_score",
        "development_potential_score"
    ]
].copy()


# =========================================================
# 16. SAVE TRACT-LEVEL LAND-USE TABLE
# =========================================================

landuse_final.to_csv(
    "data/processed/tract_landuse.csv",
    index=False
)

print()
print("Saved:")
print("data/processed/tract_landuse.csv")

print()
print("Preview:")
print(
    landuse_final
    .head(10)
    .to_string(index=False)
)
