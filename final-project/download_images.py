import requests
import os

# Google Drive file IDs (can be modified or moved to config.json)
file_ids = [
    "17QxZpfjLsL5BElf0OYNwBU0hq4wr1MG_",
    "19vAoGLwLDXrr620WHmpkNXiNwZXCVcnt",
    "1LANtLNxl5UzKY1j7gofH-kdugJeEtkLX"
]

def download_google_drive_file(file_id, dest_folder="./downloads"):
    """Downloads a single file from Google Drive"""
    os.makedirs(dest_folder, exist_ok=True)
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    file_path = os.path.join(dest_folder, f"{file_id}.jpg")
    
    print(f"Downloading {file_id}...")
    r = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(r.content)
    return file_path

# Main download execution (same as original)
local_paths = [download_google_drive_file(fid) for fid in file_ids]
print(f"Downloaded {len(local_paths)} files to {os.path.abspath('downloads')}")