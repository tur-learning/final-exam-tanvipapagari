import os
import requests
from gradio_client import Client, handle_file

# # Example images – replace these URLs with your actual image files or local paths
# # (must be at least 2 images for matching to work meaningfully)
# image_urls = [
#     "./img/pisa.jpg"  # repeat for testing
# ]

# # Convert remote image URLs into files that the client can upload
# filelist = [handle_file(url) for url in image_urls]

# Google Drive file IDs
file_ids = [
    "17QxZpfjLsL5BElf0OYNwBU0hq4wr1MG_",
    "19vAoGLwLDXrr620WHmpkNXiNwZXCVcnt",
    "1LANtLNxl5UzKY1j7gofH-kdugJeEtkLX",
    "1DEQyClx4Be_hQtq1f3xtc2X9Smz8R686",
    "1nIhExOE8asL0-7SSHx87BUij5TPxXfwj"
]

def download_google_drive_file(file_id, dest_folder="./downloads"):
    os.makedirs(dest_folder, exist_ok=True)
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    file_path = os.path.join(dest_folder, f"{file_id}.jpg")
    r = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)
    return file_path

# Download files
local_paths = [download_google_drive_file(fid) for fid in file_ids]

# Step 3: Convert local files to gradio-compatible uploads
filelist = [handle_file(path) for path in local_paths]

# Step 3: Use gradio_client to call the endpoint
HF_TOKEN = "*****"

# Initialize the client with the Space name
client = Client("tur-learning/MASt3R", hf_token=f"{HF_TOKEN}")

# Make the API call
result = client.predict(
    filelist=filelist,
    min_conf_thr=1.5,
    matching_conf_thr=2,
    as_pointcloud=True,
    cam_size=0.2,
    shared_intrinsics=False,
    api_name="/local_get_reconstructed_scene"
)

print("3D model output path:", result)
