import os
import zipfile
from PIL import Image

# 1. Original zip_images function (unchanged)
def zip_images(folder_path, zip_path):
    """Original docstring preserved"""
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    full_path = os.path.join(root, file)
                    zipf.write(full_path, arcname=file)

# 2. Original convert_png_to_jpg function (unchanged)
def convert_png_to_jpg(folder_path):
    """Original docstring preserved"""
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

# 3. Original immediate test code (if present)
if __name__ == "__main__":
    # Example test call (optional)
    zip_images("test_images", "test.zip")
    convert_png_to_jpg("test_images")