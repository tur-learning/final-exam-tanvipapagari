import os
import requests
from gradio_client import Client, handle_file
import shutil
from pathlib import Path

# Step 1: setup directory where images are stored 
# make it an option in the config. It could be
# the preprocessed dir or the downloads dir based 
# on the user choice
image_dir = "preprocessed"
local_paths = os.listdir(image_dir)
local_paths = [Path.cwd()/image_dir/file for file in local_paths]

# Step 2: Convert local files to gradio-compatible uploads
filelist = [handle_file(path) for path in local_paths]
print(filelist)

# Step 3: Use gradio_client to call the endpoint
HF_TOKEN = None

if HF_TOKEN is None:
    raise ValueError("ERROR: YOU MUST INPUT YOUR HUGGINGFACE TOKEN")

# Initialize the client with the Space name
client = Client("tur-learning/MASt3R", hf_token=f"{HF_TOKEN}")

# Make the API call
# You may want to move the most relevant parameters of the model
# to the config file, to let the user chose without modifying the code
result = client.predict(
    filelist=filelist,
    min_conf_thr=1.5,
    matching_conf_thr=2,
    as_pointcloud=False,
    cam_size=0.2,
    shared_intrinsics=False,
    api_name="/local_get_reconstructed_scene"
)

print("3D model output path:", result)

print("Copying model to model.glb file")
shutil.copyfile(result, "model.glb")
