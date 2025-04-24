import os
import zipfile
from PIL import Image
import json
import zipfile
import shutil

def zip_images(folder_path, zip_path):
    """
    Zips all image files from `folder_path` into `zip_path`, placing them
    at the root of the resulting ZIP archive.
    """
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    full_path = os.path.join(root, file)
                    zipf.write(full_path, arcname=file)


def convert_png_to_jpg(folder_path):
    """
    Convert all PNG images in 'folder_path' to JPG with a white background
    and remove the original PNG files.
    """
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(".png"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(
                folder_path,
                os.path.splitext(filename)[0] + ".jpg"
            )
            with Image.open(input_path).convert("RGBA") as img:
                white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
                white_bg.paste(img, (0, 0), img)
                rgb_img = white_bg.convert("RGB")
                rgb_img.save(output_path, "JPEG")
            os.remove(input_path)

def load_data(filename):
    """
    Loads data from a JSON file.

    Parameters:
    filename (str): The path to the JSON file.

    Returns:
    dict: Parsed JSON data.
    """
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data

# download contents of an unloaded zip file
def download_zip(zip, extract):
    zip_path = zip
    extract_folder = extract

    os.makedirs(extract_folder, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_folder)

    print(f"Files extracted to: {extract_folder}")

# add an image to downloads (filepath is path to image, id is name of image w/out suffix)
def add_photo(filepath, id):
    # copy image from dowloaded images and past into downloads
    source_file = filepath
    destination_folder = "/workspaces/final-exam-HultzHubbard/final-project/downloads"
    shutil.copy(source_file, destination_folder)

    old_file = (f"{destination_folder}/{id}.JPEG")
    new_file = old_file.replace(".JPEG", ".jpg")
    os.rename(old_file, new_file)

    # update file_ids
    json_file = "/workspaces/final-exam-HultzHubbard/final-project/config.json"
    with open(json_file, "r") as file:
        data = json.load(file)
    key = "file_ids"
    new_value = id
    if key in data and isinstance(data[key], list):
        data[key].append(new_value)
    else:
        data[key] = [new_value]
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

    # update photos.zip
    zip_file = "/workspaces/final-exam-HultzHubbard/final-project/photos.zip"
    os.remove(zip_file)
    zip_images("downloads", "photos.zip")

    print(f"{id} added to downloads")

# delete an image from downloads (filepath is path to image, id is name of image w/out suffix)
def delete_photo(filepath, id):
    file_path = filepath
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("File not found.")

    # update file_ids
    json_file = "/workspaces/final-exam-HultzHubbard/final-project/config.json"
    with open(json_file, "r") as file:
        data = json.load(file)
    key = "file_ids"
    if id in data[key]:
        data[key].remove(id)
    else:
        print(f"{id} not found in the list.")
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

    # update photos.zip
    zip_file = "/workspaces/final-exam-HultzHubbard/final-project/photos.zip"
    os.remove(zip_file)
    zip_images("downloads", "photos.zip")

    print(f"{id} has been deleted")
    
def startup():
    downloadzip = input("Is there a zip file with pictures you wish to download? (enter 'yes' or 'no'): ")
    if downloadzip == "yes":
        zippath = input("What is the name of the zip file you wish to be downloaded? (ex. 'example.zip'): ")
        downloadpath = input("What is the name of the folder you want the contents of the zip file to be downloaded to? (ex. 'example'): ")
        download_zip(zippath, downloadpath)
    else:
        print("\n")

    addtodownloads = input("Is there a photo you wish to ADD to the current photos that will be used in the program? (enter 'yes' or 'no'): ")
    while addtodownloads == "yes":
        imagepath = input("Please input the image path here (ex. '/your/image/path/here'): ")
        imageid = input("Please input the name of the image (ex. 'IMG_1111'): ")
        add_photo(imagepath, imageid)
        addtodownloads = input("Is there another photo you wish to ADD to the current photos that will be used in the program? (enter 'yes' or 'no'): ")
        if addtodownloads == "no":
            print("\n")

    deletefromdownloads = input("Is there a photo you wish to DELETE to the current photos that will be used in the program? (enter 'yes' or 'no'): ")
    while deletefromdownloads == "yes":
        imagepath = input("Please input the image path here (ex. '/your/image/path/here'): ")
        imageid = input("Please input the name of the image (ex. 'IMG_1111'): ")
        delete_photo(imagepath, imageid)
        deletefromdownloads = input("Is there another photo you wish to DELETE to the current photos that will be used in the program? (enter 'yes' or 'no'): ")
        if deletefromdownloads == "no":
            print("\n")

def inputconfig():
    # define the json file path
    json_file = "config.json"
    # load existing json data
    try:
        with open(json_file, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}  # If the file doesn't exist, start with an empty dictionary
    # set all values to "false"
    key1 = "preprocess_image"
    key2 = "use_mast3r"
    key3 = "use_dust3r"
    value = False
    # reset json data
    data[key1] = value
    data[key2] = value
    data[key3] = value
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

    # get user input about if they want to use processed images
    print("There are two factors you need to input. Please answer as indicated.\n")
    key = "preprocess_image"
    init = input("Would you like to use processed images (images with the background removed)? If so, enter 'yes'. Else enter 'no': ")
    while init not in ["yes", "no"]:
        init = input("You must enter either 'yes' or 'no'. Would you like to use processed images (images with the background removed)?: ")
    if init == "yes":
        value = True
    elif init == "no":
        value = False
    # update json data
    data[key] = value
    # save the changes
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)

    # get user input about which 3D processer they want to use
    init = ""
    while init not in ["mast3r", "dust3r"]:
        init = input("\nWhich 3D image generator do you wish to use, mast3r or dust3r? (you must answer with either mast3r or dust3r): ")
    if init == "mast3r":   
        key = "use_mast3r"
        value = True
    elif init == "dust3r":
        key = "use_dust3r"
        value = True
    else:
        input("Which 3D image generator do you wish to use, mast3r or dust3r? (you must answer with either mast3r or dust3r): ")
    # update json data
    data[key] = value
    # save the changes
    with open(json_file, "w") as file:
        json.dump(data, file, indent=4)
        
    print("Information updated successfully!")