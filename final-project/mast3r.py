import os
import requests
from gradio_client import Client, handle_file
import shutil
from pathlib import Path

# Original variable names and structure
image_dir = "preprocessed"  # Original hardcoded path
local_paths = [Path.cwd()/image_dir/file for file in os.listdir(image_dir)]
filelist = [handle_file(path) for path in local_paths]

# Original client setup
HF_TOKEN = None  # As in original code
if HF_TOKEN is None:
    raise ValueError("ERROR: YOU MUST INPUT YOUR HUGGINGFACE TOKEN")

client = Client("tur-learning/MASt3R", hf_token=f"{HF_TOKEN}")

# Original API call with hardcoded parameters
result = client.predict(
    filelist=filelist,
    min_conf_thr=1.5,       # Original hardcoded value
    matching_conf_thr=2,     # Original hardcoded value
    as_pointcloud=False,     # Original hardcoded value
    cam_size=0.2,           # Original hardcoded value
    shared_intrinsics=False, # Original hardcoded value
    api_name="/local_get_reconstructed_scene"
)

# Original output handling
print("3D model output path:", result)
print("Copying model to model.glb file")
shutil.copyfile(result, "model.glb")  # Original hardcoded output
