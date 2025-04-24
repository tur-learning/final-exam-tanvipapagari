# ----------------------------------------------------------------------------------
# Example Python Script: Demonstrating a Simple Workflow with gradio_client
# ----------------------------------------------------------------------------------

# We import "Client" to interact with the remote Gradio app.
# "handle_file" help us upload local or remote files to the app.
from gradio_client import Client, handle_file
import shutil
import os
from utils import convert_png_to_jpg

# Original hardcoded variables
YOUR_TOKEN = None  # Same variable name as original
if YOUR_TOKEN is None:
    raise ValueError("ERROR: YOU MUST INPUT YOUR HUGGINGFACE TOKEN")

# Original client initialization
client = Client("tur-learning/TRELLIS", hf_token=YOUR_TOKEN)

# Original session start
client.predict(api_name="/start_session")

# Original image processing
image_path = None  # Same as original
if image_path is None:
    raise ValueError("ERROR: YOU MUST INPUT A VALID IMAGE PATH")

# Original API call
processed_image = client.predict(
    image=handle_file(image_path),
    api_name="/preprocess_image"
)

print("Server returned path:", processed_image)  # Original output