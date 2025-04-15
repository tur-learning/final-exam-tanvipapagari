import time
from osm_client import OpenStreetMapClient

# Initialize OSM client
client = OpenStreetMapClient()

###############################
# 1) Define Map Metadata
###############################
attributes = {
    "Fileformat": "png",
    "Scale": 5000,
    "PrintWidth": 600,
    "PrintHeight": 600,
    "Latitude": 41.89247, 
    "Longitude": 12.47316,
    "Style": "osm-carto",
    "Projection": "3857",
    "HideLayers": "admin-low-zoom,admin-mid-zoom,admin-high-zoom,admin-text",
    "UserObjects": [
        { # White frame
            "Style": "<PolygonSymbolizer fill='white' fill-opacity='1.0' />",
            "WellKnownText": "POLYGON((0.0 0.0, 0.0 600.0, 600.0 600.0, 600.0 0.0, 0.0 0.0), (20.0 20.0, 20.0 580.0, 580.0 580.0, 580.0 20.0, 20.0 20.0))"
        },
        {
            "Style": "<LineSymbolizer stroke='dimgray' stroke-width='1.0' stroke-linecap='square' />",
            "WellKnownText": "LINESTRING(20.0 20.0, 20.0 580.0, 580.0 580.0, 580.0 20.0, 20.0 20.0)"
        },
        { # Writing
            "Style": "<TextSymbolizer fontset-name='fontset-2' size='80' fill='dimgray' opacity='0.6' allow-overlap='true'>'Rome'</TextSymbolizer>",
            "WellKnownText": "POINT(90.0 560.0)"
        },
        {
            "Style": "<TextSymbolizer fontset-name='fontset-0' size='12' fill='dimgray' orientation='90' allow-overlap='true'>'© OpenStreetMap contributors'</TextSymbolizer>",
            "WellKnownText": "POINT(11 300.0)"
        }
    ]
}

###############################
# 2) Create Map Metadata
###############################
metadata_response = client.create_map_metadata(attributes)
map_id = metadata_response.get("Data", {}).get("ID", "")

if not map_id:
    print("Error: No map ID received. Exiting.")
    exit()

###############################
# 3) Order the Map
###############################
order_response = client.order_map(map_id)

###############################
# 4) Wait for Map Processing
###############################
map_build_successful = "no"
timeout_minutes = 5
timeout_sleep = int(timeout_minutes)
start_time = time.time()
timeout_seconds = timeout_minutes * 60

while map_build_successful != "yes" and (time.time() - start_time) < timeout_seconds:
    map_state = client.fetch_map_state(map_id)
    map_build_successful = map_state.get("Data", {}).get("Attributes", {}).get("MapBuildSuccessful", "no")

    if map_build_successful != "yes":
        print(f"Build ({map_id}) not successful yet, waiting for {timeout_sleep} second(s)...")
        time.sleep(timeout_sleep)

###############################
# 5) Download the Map
###############################
if map_build_successful == "yes":
    print("Build is successful, downloading the map...")
    client.download_map(map_id)
else:
    print(f"Build was not successful within {timeout_minutes} minutes.")
