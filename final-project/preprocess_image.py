# ----------------------------------------------------------------------------------
# Example Python Script: Demonstrating a Simple Workflow with gradio_client
# ----------------------------------------------------------------------------------

# We import "Client" to interact with the remote Gradio app.
# "handle_file" help us upload local or remote files to the app.
from gradio_client import Client, handle_file
import shutil

YOUR_TOKEN = None # COPY YOUR HF TOKEN HERE

if YOUR_TOKEN is None:
    raise ValueError("ERROR: YOU MUST INPUT YOUR HUGGINGFACE TOKEN")

# Create a client object that points to the Gradio (Hugging Face) Space where our app runs.
# "secret_key" is your Hugging Face token if the Space is private or requires authentication.
client = Client("tur-learning/TRELLIS", hf_token=YOUR_TOKEN)

# 1. Start a session on the remote app (optional in many cases, but some apps require it).
#    This can create a dedicated folder or initialize user-specific state on the server side.
client.predict(api_name="/start_session")

# 2. Preprocess an image for the pipeline.
#    "handle_file(path_to_image)" tells the client to either upload a local file or download
#    from a remote URL, so the server will receive it in the correct format for the "image" input.

image_path = None # COPY IMAGE PATH HERE

if image_path is None:
    raise ValueError("ERROR: YOU MUST INPUT A VALID IMAGE PATH")

processed_image = client.predict(
    image=handle_file(image_path),
    api_name="/preprocess_image"
)
print("Server returned path:", processed_image)