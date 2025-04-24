from gradio_client import Client, handle_file
import os
import shutil
from pathlib import Path
from utils import convert_png_to_jpg

# Original hardcoded variables
root = "downloads"  # Same as original
images_path = os.listdir(root)  # Original immediate execution

# Original client initialization
client = Client("KenjieDec/RemBG")  # Same model as original

# Original directory setup
preprocessed_dir = Path("preprocessed").resolve()
shutil.rmtree(preprocessed_dir)  # Original cleanup
Path.mkdir(preprocessed_dir)  # Original directory creation

# Original processing loop
for image in images_path:
    # Original API call with hardcoded parameters
    result = client.predict(
        file=handle_file(os.path.join(root, image)),
        mask="Default",  # Original hardcoded
        model="u2netp",  # Original hardcoded
        x=3,  # Original hardcoded
        y=3,  # Original hardcoded
        api_name="/inference"  # Original endpoint
    )
    
    # Original file handling
    result = Path(result)
    print(result)  # Original debug print
    print("Copying preprocessed image to 'preprocessed' directory")
    shutil.copyfile(result, os.path.join("preprocessed", result.parent.name+result.suffix))

# Original conversion
convert_png_to_jpg(preprocessed_dir) 