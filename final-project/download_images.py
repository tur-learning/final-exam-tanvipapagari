import requests
import os
from utils import load_data

x = load_data("config.json")
file_ids = x.get("file_ids")

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