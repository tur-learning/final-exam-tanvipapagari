# 1
# Import necessary modules
import json
from download_images import download_google_drive_file, file_ids
from dust3r import send_request
from mast3r import make3D
from preprocess import preprocess
from utils import load_data, startup, inputconfig
import subprocess

# To download the info from photos.zip
# for i in file_ids:
#     download_google_drive_file(i)

# startup functions (download a new zip, add/delete photos from downloads)
startup()



# ----------------------------------------------------------------------------------------------------------------------------------
# 2
# input config.json to read configurations

inputconfig()

# -------------------------------------------------------------------------------------------------------------------------------------

# # 3
# # get user input on configured parameters

config = load_data("config.json")

dust3r = config.get("use_dust3r", None)
mast3r = config.get("use_mast3r", None)
preprocessing = config.get("preprocess_image", None)

print("\nStarting 3D image generation\n")

if preprocessing == False:
    if dust3r == True:
        print("We are going to use dust3r APIs")
        send_request("photos.zip")
    if mast3r == True:
        print("We are going to use mast3r APIs")
        make3D("raw")
elif preprocessing == True:
    print("We are going to preprocess the image to remove the background")
    preprocess()
    if dust3r == True:
        print("We are going to use dust3r APIs")
        send_request("processed_images.zip")
    if mast3r == True:
        print("We are going to use mast3r APIs")
        make3D("process")

# run "python -m http.server"
subprocess.run(["python", "-m", "http.server", "8000"])