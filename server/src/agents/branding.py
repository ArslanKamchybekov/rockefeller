import google.generativeai as genai
import base64
import io
from PIL import Image
from typing import Optional, Dict, Any
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.branding import BrandingInfoInput, BrandingInfoOutput

api_key = "AIzaSyCWogjxlcxSgZkV5KfZllfZr2tssq8PzUI"


# from google import genai
# from google.genai import types
# from PIL import Image
# from io import BytesIO

# client = genai.Client()

# prompt = (
#     "Create a picture of a nano banana dish in a fancy restaurant with a Gemini theme"
# )

# response = client.models.generate_content(
#     model="gemini-2.5-flash-image-preview",
#     contents=[prompt],
# )

# for part in response.candidates[0].content.parts:
#     if part.text is not None:
#         print(part.text)
#     elif part.inline_data is not None:
#         image = Image.open(BytesIO(part.inline_data.data))
#         image.save("generated_image.png")

class BrandingAgent:
    """Agent responsible for generating branding materials using Google's Gemini AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the branding agent with API key."""
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        genai.configure(api_key=self.api_key)
        self.text_model = genai.GenerativeModel('gemini-2.0-flash')
        self.image_model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
    
    async def generate_branding(self, market_data: str) -> BrandingInfoOutput:
        """
        Generate branding materials (logo, name, slogan) based on market data.
        
        Args:
            market_data: Market research data and context for the business
            
        Returns:
            BrandingInfoOutput containing generated logo, name, and slogan
        """
        result = {
            "image": None,
            "name": None,
            "slogan": None
        }
        
        try:
            # Generate logo prompt and create logo
            logo_prompt = await self._process_text(
                "Create a detailed prompt for a professional logo design based on this business context. "
                "The prompt should specify colors, style (modern, classic, minimalist, etc.), and visual elements. "
                "Make it suitable for a logo generation AI. Context: ", 
                market_data
            )
            
            # Generate the logo image with the AI-generated prompt
            full_logo_prompt = f"Create a professional logo design: {logo_prompt}"
            logo_response = await self._generate_image(full_logo_prompt)
            result["image"] = logo_response
            
            # Generate business name
            result["name"] = await self._process_text(
                "Generate me only one (don't give me options) an at most 3 word name for the business "
                "given the context of this market data: ", 
                market_data
            )
            
            # Generate slogan
            result["slogan"] = await self._process_text(
                "Generate me only one (don't give me options) a short phrase slogan for the business "
                "given the context of the market data: ", 
                market_data
            )
            
        except Exception as e:
            print(f"Error generating branding: {e}")
            # Return partial results if some operations fail
            pass
        
        return BrandingInfoOutput(**result)
    
    async def _process_text(self, context: str, market_data: str) -> str:
        """Process text using Gemini AI."""
        try:
            response = self.text_model.generate_content(f"{context} {market_data}")
            return response.text.strip()
        except Exception as e:
            print(f"Error processing text: {e}")
            return ""
    
    async def _generate_image(self, prompt: str) -> Optional[bytes]:
        """Generate an image using Gemini AI."""
        try:
            # Use the image generation model with proper prompt
            response = self.image_model.generate_content(prompt)
            
            # Process the response to extract image data
            if hasattr(response, 'candidates') and response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # The image data is already in bytes format
                        return part.inline_data.data
            
            return None
            
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
    
    def save_logo(self, image_data: bytes, filename: str = "generated_logo.png") -> str:
        """Save generated logo to file."""
        try:
            with open(filename, 'wb') as f:
                f.write(image_data)
            return filename
        except Exception as e:
            print(f"Error saving logo: {e}")
            return ""


async def main():
    """Example usage of the BrandingAgent."""
    try:
        agent = BrandingAgent(api_key=api_key)
        result = await agent.generate_branding("Lollipops and candy business")
        
        if result.image:
            filename = agent.save_logo(result.image)
            print(f"Logo saved as: {filename}")
        
        print(f"Business name: {result.name}")
        print(f"Slogan: {result.slogan}")
        
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())