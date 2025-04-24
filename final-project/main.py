# 1
# Import necessary modules
import json
import download_images
import preprocess
import dust3r
import mast3r

# Read config file
with open("config.json") as f:
    config = json.load(f)

# Implement logic based on configured parameters
if config["preprocess_image"]:
    print("Preprocessing images to remove background")
    preprocessed_images = preprocess.remove_background(
        input_dir="downloads",
        output_dir="preprocessed"
    )

if config["use_dust3r"]:
    print("Using dust3r APIs")
    dust3r.generate_model(
        image_dir="preprocessed",
        output_path="model.glb"
    )

if config["use_mast3r"]:
    print("Using mast3r APIs")
    mast3r.generate_model(
        image_dir="preprocessed",
        output_path="model.glb",
        hf_token=config["mast3r"]["hf_token"]
    )

print("Processing complete")
# 3
# implement logic to use different models based on the configured parameters
