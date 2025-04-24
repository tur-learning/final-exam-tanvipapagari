from utils import (
    extract_files, load_data, find_best_matches,
    save_to_json, save_to_geojson
)

# File paths
zip_path = "geojson_data.zip"  # Change if your zip file has a different name or path
extract_path = "geojson_data"
nolli_file = "nolli_points_open.geojson"
osm_file = "osm_node_way_relation.geojson"

# Step 1: Extract files
extracted_files = extract_files(zip_path, [nolli_file, osm_file], extract_path)
nolli_path, osm_path = extracted_files

# Step 2: Load data
nolli_data = load_data(nolli_path)
osm_data = load_data(osm_path)

# Step 3: Prepare Nolli data
nolli_relevant_data = {}

for feature in nolli_data["features"]:
    props = feature["properties"]
    nolli_id = str(props.get("Nolli Number", "")).strip()
    
    # Collect non-empty and non-"n/a" names
    names = [
        props.get("Nolli Name", ""),
        props.get("Unravelled Name", ""),
        props.get("Modern Name", "")
    ]
    names = [name for name in names if name and name.lower() != "n/a"]

    nolli_relevant_data[nolli_id] = {
        "nolli_names": names,
        "nolli_coords": feature.get("geometry")
    }

# Step 4: Perform fuzzy matching
osm_features = osm_data["features"]

for nolli_id, values in nolli_relevant_data.items():
    match, count = find_best_matches(
        values["nolli_names"],
        osm_features,
        key_field="name",
        threshold=85,
        scorer="partial_ratio"
    )
    nolli_relevant_data[nolli_id]["match"] = match if count > 0 else None

# Step 5: Save results
save_to_json(nolli_relevant_data, "matched_nolli_features.json")
save_to_geojson(nolli_relevant_data, "matched_nolli_features.geojson")
