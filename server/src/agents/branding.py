from src.utils.create_gemini import create_gemini_client, create_gemini_image_client
import json

def generate_branding (idea_string: str) -> dict:
    """
    Generates branding assets based on the provided idea string.

    Args:
        idea_string (str): The idea or concept for which to generate branding assets.

    Returns:
        dict: A dictionary containing the generated branding assets.
    """
    try:

        client = create_gemini_client()
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
        """

        response = client.generate_content(
            prompt,
            generation_config={"temperature": 0.7},
        )

        branding_data = json.loads(response.text)
        result.update(branding_data)

        imageClient = create_gemini_image_client()
        image_prompt = f"Create a logo for a brand named '{result['brand_name']}' with the tagline '{result['tagline']}'. The logo should be modern and visually appealing."
        image_response = imageClient.generate_image(
            image_prompt,
            image_config={"height": 512, "width": 512, "num_images": 1}
        )
        result['logo'] = image_response.images[0].uri

        return { "branding": result }
    
    except Exception as e:
        print(f"Error processing branding data: {e}")
        return { "branding": response.text }
    
