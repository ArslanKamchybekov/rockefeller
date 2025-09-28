from src.utils.create_openai import create_openai_client
from src.utils.create_gemini import create_gemini_client, create_gemini_video_client
import json
import re
import time
import requests
import base64

def generate_branding (idea_string: str) -> dict:
    """
    Generates branding assets based on the provided idea string.

    Args:
        idea_string (str): The idea or concept for which to generate branding assets.

    Returns:
        dict: A dictionary containing the generated branding assets.
    """
    try:
        print("Generating branding assets for: ", idea_string)

        MODEL, client = create_gemini_client()
        result = {
            "brand_name": "",
            "tagline": "",
            "logo": "",
        }
        prompt = f"""
            You are a branding expert. Generate a set of branding assets based on the following idea:
            IDEA: {idea_string}
            Output a JSON object with the following fields:
            - brand_name: A catchy and relevant brand name.
            - tagline: A short and memorable tagline.
            Do not include any code markdown (like ```json) or other text outside the JSON object.
        """

        print("Prompt: ", prompt)

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )


        raw = response.text.strip()
        cleaned = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
        
        print("Cleaned: ", cleaned)

        branding_data = json.loads(cleaned)

        print("Generated branding data: ", branding_data)

        result.update(branding_data)
        
        print("Generating logo...")
        client = create_openai_client()

        image_prompt = f"Create a logo for a brand named '{result['brand_name']}' with the tagline '{result['tagline']}'. The logo should be modern and visually appealing."
        image_response = client.images.generate(
            model="dall-e-2",
            prompt=image_prompt,
            n=1,
            size="1024x1024",
        )

        image_data = image_response.data[0]    
        
        with open("branding_photo.png", "wb") as f:
            f.write(base64.b64decode(image_data))

        print("Generated logo!")

        return { "branding": result }
    
    except Exception as e:
        print(f"Error processing branding data: {e}")
        return { "branding": response.text }

def generate_branding_video(idea_string: str) -> dict:
    """
    Generates a branding video based on the provided idea string.
    """
    try:
        print("Generating branding video for: ", idea_string)

        VIDEO_MODEL, client = create_gemini_video_client()
        prompt = f"""
            You are a branding expert. Generate a branding video based on the following idea:
            IDEA: {idea_string}
        """

        operation = client.models.generate_videos(
            model=VIDEO_MODEL,
            prompt=prompt,
        )

        while not operation.done:
            print("Waiting for video to be generated...")
            time.sleep(10)
            operation = client.operations.get(operation)

        generated_video = operation.response.generated_videos[0]
        client.files.download(file=generated_video.video)
        generated_video.video.save("branding_video.mp4")

        return { "video": True }
    except Exception as e:
        print(f"Error processing branding video: {e}")
        return { "video": None }
    
