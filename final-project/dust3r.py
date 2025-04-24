import requests
import os
from utils import zip_images

def send_request(glb_file_path):
    """Sends request to dust3r API endpoint (original function)"""
    print("Sending request to HuggingFace endpoint")
    url = "https://tur-learning-dust3r-fastapi.hf.space/upload_zip/"
    output_file_path = "model.glb"  # Original hardcoded path

    # Load the file
    with open(glb_file_path, "rb") as f:
        files = {'file': f}
        response = requests.post(url, files=files)

    # Save the response
    if response.status_code == 200:
        with open(output_file_path, "wb") as f:
            f.write(response.content)
        print("File saved as model.glb")
    else:
        print(f"Error: {response.status_code}")

# Original execution block
if __name__ == "__main__":
    image_dir = "preprocessed"  # Original hardcoded path
    zip_images(image_dir, "photos.zip")  # Original zip filename
    send_request("photos.zip")  # Original function call