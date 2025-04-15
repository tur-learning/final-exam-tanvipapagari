# ----------------------------------------------------------------------------------
# Example Python Script: Demonstrating a Simple Workflow with gradio_client
# ----------------------------------------------------------------------------------

# We import "Client" to interact with the remote Gradio app.
# "handle_file" help us upload local or remote files to the app.
from gradio_client import Client, handle_file
import shutil

YOUR_TOKEN = ... # COPY YOUR HF TOKEN HERE

# Create a client object that points to the Gradio (Hugging Face) Space where our app runs.
# "secret_key" is your Hugging Face token if the Space is private or requires authentication.
client = Client("turome-learning/TRELLIS", hf_token=YOUR_TOKEN)

# 1. Start a session on the remote app (optional in many cases, but some apps require it).
#    This can create a dedicated folder or initialize user-specific state on the server side.
client.predict(api_name="/start_session")

# 2. Preprocess an image for the pipeline.
#    "handle_file(path_to_image)" tells the client to either upload a local file or download
#    from a remote URL, so the server will receive it in the correct format for the "image" input.

image_path = ... # COPY IMAGE PATH HERE

processed_image = client.predict(
    image=handle_file(image_path),
    api_name="/preprocess_image"
)
print("Server returned path:", processed_image)

# 3. Decide on a random or fixed seed for the 3D generation.
#    Here, we are asking the server to randomize the seed, but specifying "42" as a fallback.
#    The final seed used by the server is returned. 
final_seed = client.predict(
    randomize_seed=True,  # if True, the server picks a random seed
    seed=42,              # if randomize_seed=False, this would be used
    api_name="/get_seed"
)

# 4. Run the main 3D pipeline to generate a model/video preview.
#    This endpoint needs the (processed) image, seed, and various other parameters 
#    (e.g., guidance strengths and sampling steps). 
#    For multi-image mode, we could pass more images via "multiimages=".
result = client.predict(
    # "handle_file(processed_image)" re-uploads the local file returned from step 2
    # so the server can use it as input to the 3D pipeline.
    image=handle_file(processed_image),
    seed=final_seed,
    ss_guidance_strength=7.5,
    ss_sampling_steps=12,
    slat_guidance_strength=3,
    slat_sampling_steps=12,
    multiimage_algo="stochastic",
    api_name="/image_to_3d"  # The endpoint that converts images -> 3D + video
)

# "result" here typically includes the path to the generated video or any other outputs.
# The exact content depends on the Gradio app definition.
print(result)

# 5. If we want a single-step pipeline that directly returns a .glb file (no video),
#    we can call a specialized endpoint, "/image_to_glb".
#    This function in the server code:
#       1) Preprocesses + runs the pipeline
#       2) Extracts the GLB
#       3) Returns the path to the GLB
result = client.predict(
    image=handle_file(processed_image),
    # multiimages=handle_file([processed_image1, processed_image2]),
    seed=0,
    ss_guidance_strength=7.5,
    ss_sampling_steps=12,
    slat_guidance_strength=3,
    slat_sampling_steps=12,
    multiimage_algo="stochastic",
    mesh_simplify=0.95,
    texture_size=1024,
    api_name="//image_to_glb"
)
print(result)

shutil.copyfile(result, "result.glb")
