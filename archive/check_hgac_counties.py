import requests

url = (
    "https://gis.h-gac.com/arcgis/rest/services/"
    "Land_Use/Current_Land_Use/MapServer/0/query"
)

params = {
    "where": "1=1",
    "outFields": "County,ParcelID",
    "returnGeometry": "false",
    "resultRecordCount": 200,
    "orderByFields": "OBJECTID ASC",
    "f": "json"
}

print("Requesting small H-GAC sample...")

response = requests.get(
    url,
    params=params,
    timeout=30
)

response.raise_for_status()

data = response.json()

if "error" in data:
    print(data)
    raise SystemExit

features = data.get("features", [])

print("Rows returned:", len(features))

counties = sorted(
    {
        f["attributes"].get("County")
        for f in features
        if f["attributes"].get("County") is not None
    }
)

print("County values found:")
for county in counties:
    print(repr(county))

print()
print("First 20 rows:")

for feature in features[:20]:
    print(feature["attributes"])
    