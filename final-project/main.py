# 1
# Import necessary modules
import json
import server

# 2
# input config.json to read configurations
with open("config.json") as f:
    config = json.load(f)


# 3
# implement logic to use different models based on the configured parameters
if config["preprocess_image"]:
    print("We are going to preprocess the image to remove the background")

if config["use_dust3r"]:
    print("We are going to use dust3r APIs")

if config["use_mast3r"]:
    print("We are going to use mast3r APIs")