from src.utils.create_openai import create_openai_client
from src.utils.create_gemini import create_gemini_client, create_gemini_video_client
import json
import re
import time
import requests
import base64
import os
import uuid
from supabase import create_client, Client

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

        image_prompt = f"""
        Create a logo for a brand named '{result['brand_name']}' with the tagline '{result['tagline']}'. The logo should be modern and visually appealing. No text.
        """
        image_response = client.images.generate(
            model="dall-e-2",
            prompt=image_prompt,
            n=1,
            size="1024x1024",
        )

        image_url = image_response.data[0].url
        
        # Download the image from the URL
        image_response_download = requests.get(image_url)
        image_response_download.raise_for_status()
        
        # No local save; we will upload bytes directly to Supabase Storage

        # Upload to Supabase Storage using service role key
        try:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            bucket_name = os.getenv("SUPABASE_BUCKET", "product_images")
            if not supabase_url or not supabase_service_key:
                raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY env vars")

            sb: Client = create_client(supabase_url, supabase_service_key)
            object_key = f"logos/{result['brand_name'].strip().lower().replace(' ', '-')}-{uuid.uuid4().hex}.png"

            # Upload bytes to Supabase Storage
            upload_res = sb.storage.from_(bucket_name).upload(
                path=object_key,
                file=image_response_download.content,
                file_options={"contentType": "image/png", "upsert": "true"},
            )
            # UploadResponse object doesn't have .get() method, check for errors differently
            if hasattr(upload_res, 'error') and upload_res.error:
                raise RuntimeError(upload_res.error)

            # Get public URL
            public = sb.storage.from_(bucket_name).get_public_url(object_key)
            public_url = public.get("publicUrl") if isinstance(public, dict) else None
            if not public_url:
                # Fallback to generated URL pattern
                public_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{object_key}"
            result["logo"] = public_url
        except Exception as supa_e:
            print(f"Error uploading logo to Supabase Storage: {supa_e}")

        print("Generated logo and uploaded to Supabase Storage!")

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

        # Guard against missing/empty responses
        response = getattr(operation, 'response', None)
        videos = getattr(response, 'generated_videos', None) if response else None
        if not videos or len(videos) == 0:
            print("Video generation returned no videos.")
            return { "video": False }

        generated_video = videos[0]
        from io import BytesIO
        video_bytes = None
        try:
            downloaded = client.files.download(file=generated_video.video)
            # Handle different SDK return types gracefully
            if isinstance(downloaded, (bytes, bytearray)):
                video_bytes = bytes(downloaded)
            elif hasattr(downloaded, "read"):
                video_bytes = downloaded.read()
            elif hasattr(generated_video.video, "bytes"):
                video_bytes = generated_video.video.bytes  # type: ignore[attr-defined]
            else:
                # Last resort: attempt to use .save into an in-memory buffer if supported
                buffer = BytesIO()
                if hasattr(generated_video.video, "save"):
                    try:
                        generated_video.video.save(buffer)  # type: ignore[call-arg]
                        buffer.seek(0)
                        video_bytes = buffer.read()
                    except Exception:
                        pass
            if not video_bytes:
                raise RuntimeError("Unable to retrieve generated video bytes from Gemini client")
        except Exception as dl_e:
            print(f"Error saving generated video: {dl_e}")
            return { "video": False, "video_url": None }

        # Upload saved video to Supabase Storage and return public URL
        try:
            supabase_url = os.getenv("SUPABASE_URL")
            supabase_service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
            bucket_name = os.getenv("SUPABASE_BUCKET", "product_images")
            if not supabase_url or not supabase_service_key:
                raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY env vars")

            sb: Client = create_client(supabase_url, supabase_service_key)
            safe_name = re.sub(r"[^a-z0-9-]", "-", idea_string.strip().lower().replace(" ", "-"))[:60]
            object_key = f"videos/{safe_name}-{uuid.uuid4().hex}.mp4"

            # video_bytes already populated above

            upload_res = sb.storage.from_(bucket_name).upload(
                path=object_key,
                file=video_bytes,
                file_options={"contentType": "video/mp4", "upsert": "true"},
            )
            if hasattr(upload_res, 'error') and upload_res.error:
                raise RuntimeError(upload_res.error)

            public = sb.storage.from_(bucket_name).get_public_url(object_key)
            public_url = public.get("publicUrl") if isinstance(public, dict) else None
            if not public_url:
                public_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{object_key}"

            return { "video": True, "video_url": public_url }
        except Exception as supa_e:
            print(f"Error uploading video to Supabase Storage: {supa_e}")
            return { "video": True, "video_url": None }
    except Exception as e:
        print(f"Error processing branding video: {e}")
        return { "video": False }
    
