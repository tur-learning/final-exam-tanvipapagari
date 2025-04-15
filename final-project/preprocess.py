from gradio_client import Client, handle_file
import os, shutil
from pathlib import Path
from utils import convert_png_to_jpg

# This variable can be put in the config file
root = "downloads"
images_path = os.listdir(root)

# Visit this page to view the possible models that can be used:
# https://huggingface.co/spaces/KenjieDec/RemBG
client = Client("KenjieDec/RemBG")

preprocessed_dir = Path("preprocessed").resolve()
# Initially removes dir
shutil.rmtree(preprocessed_dir)
Path.mkdir(preprocessed_dir)

for image in images_path:
    result = client.predict(
            file=handle_file(os.path.join(root, image)),
            mask="Default",
            model="u2netp", # You can change the model if you wish, or add it as a config parameter
            x=3,
            y=3,
            api_name="/inference"
    )
    result = Path(result)
    print(result)
    print("Copying preprocessed image to 'preprocessed' directory")
    shutil.copyfile(result, os.path.join("preprocessed", result.parent.name+result.suffix))

# Images are converted to jpg for integration with dust3r model
convert_png_to_jpg(preprocessed_dir)