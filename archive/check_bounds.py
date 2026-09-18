import geopandas as gpd

landuse = gpd.read_file(
    "data/raw/landuse/hgac_current_landuse.geojson"
)

tracts = gpd.read_file(
    "data/processed/houston_urban_dna.geojson"
)

print("LAND USE")
print("CRS:", landuse.crs)
print("Bounds:", landuse.total_bounds)

print()

print("TRACTS")
print("CRS:", tracts.crs)
print("Bounds:", tracts.total_bounds)

print()

print("Sample land-use geometry:")
print(landuse.geometry.iloc[0])

print()

print("Sample tract geometry:")
print(tracts.geometry.iloc[0])