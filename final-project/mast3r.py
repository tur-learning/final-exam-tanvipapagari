import os
from gradio_client import Client, handle_file
import shutil
from download_images import download_google_drive_file, file_ids
import zipfile

def make3D(input):
    # Download files
    if input == "process":
        extract_dir = "preprocessed"
        with zipfile.ZipFile("/workspaces/final-exam-tanvipapagari/final-project/processed_images.zip", "r") as zip_ref:
            zip_ref.extractall(extract_dir)
            print(f"Extracted files to {extract_dir}")
        local_paths = [os.path.join(extract_dir, fname) for fname in os.listdir(extract_dir)]
    elif input == "raw":
        local_paths = [download_google_drive_file(fid) for fid in file_ids]

    # Step 3: Convert local files to gradio-compatible uploads
    filelist = [handle_file(path) for path in local_paths]

    # Step 3: Use gradio_client to call the endpoint
    HF_TOKEN = "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"

    if HF_TOKEN is None:
        raise ValueError("ERROR: YOU MUST INPUT YOUR HUGGINGFACE TOKEN")
    
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

    shutil.copyfile(result, "model.glb")