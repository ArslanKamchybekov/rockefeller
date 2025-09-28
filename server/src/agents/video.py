import time
import os
import sys
from typing import Optional, Tuple, Any
from datetime import datetime
import asyncio

# Add the parent directory to the path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models.video import VideoInput, VideoOutput, VideoRequest, VideoResponse

api_key = "AIzaSyCWogjxlcxSgZkV5KfZllfZr2tssq8PzUI"

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Warning: google-genai package not installed. Video generation will not work.")
    genai = None


class VideoAgent:
    """Agent responsible for generating videos using Google's Veo AI."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the video agent with API key."""
        if genai is None:
            raise ImportError("google-genai package is required for video generation")
            
        self.api_key = api_key or globals()['api_key'] or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is required. Set GOOGLE_API_KEY environment variable.")
        
        self.client = genai.Client(api_key=self.api_key)
    
    async def generate_video(self, prompt: str, duration: int = 10, quality: str = "high") -> VideoOutput:
        """
        Generate a video based on the given prompt.
        
        Args:
            prompt: Text description of the video to generate
            duration: Video duration in seconds (default: 10)
            quality: Video quality - low, medium, high (default: high)
            
        Returns:
            VideoOutput containing the generated video data
        """
        try:
            # Start the video generation
            operation = self.client.models.generate_videos(
                model="veo-3.0-generate-001",
                prompt=prompt,
            )

            # Poll the operation status until the video is ready
            while not operation.done:
                print("Waiting for video generation to complete...")
                await asyncio.sleep(10)  # Use async sleep
                operation = self.client.operations.get(operation)

            # Ensure the operation successfully generated a video
            if not operation.response.generated_videos:
                raise Exception("Video generation failed or returned no video.")

            generated_video = operation.response.generated_videos[0]
            
            # Create a unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_video_{timestamp}.mp4"
            temp_file_path = f"temp_{filename}"
            
            # Download and save the file temporarily
            self.client.files.download(file=generated_video.video)
            generated_video.video.save(temp_file_path)

            # Read the saved file into a binary buffer
            with open(temp_file_path, 'rb') as video_file:
                video_data = video_file.read()
            
            # Clean up the temporary local file
            os.remove(temp_file_path)
            
            print(f"Successfully generated video: {filename}")
            
            return VideoOutput(
                video_data=video_data,
                filename=filename,
                duration=duration,
                created_at=datetime.utcnow()
            )
            
        except Exception as e:
            print(f"Error generating video: {e}")
            return VideoOutput(
                video_data=None,
                filename=None,
                duration=None,
                created_at=datetime.utcnow()
            )
    
    def save_video(self, video_data: bytes, filename: str) -> str:
        """Save video data to a file."""
        try:
            with open(filename, 'wb') as f:
                f.write(video_data)
            return filename
        except Exception as e:
            print(f"Error saving video: {e}")
            return ""
    
    def generate_video_sync(self, prompt: str, duration: int = 10, quality: str = "high") -> VideoOutput:
        """Synchronous version of video generation."""
        return asyncio.run(self.generate_video(prompt, duration, quality))


def generate_video_operation(prompt: str) -> Tuple[Any, Any]:
    """
    Generates the video and polls the operation until complete.
    Legacy function for backward compatibility.

    Returns:
        A tuple containing the client and the final operation object.
    """
    if genai is None:
        raise ImportError("google-genai package is required")
        
    client = genai.Client()
    
    # Start the video generation
    operation = client.models.generate_videos(
        model="veo-3.0-generate-001",
        prompt=prompt,
    )

    # Poll the operation status until the video is ready.
    while not operation.done:
        print("Waiting for video generation to complete...")
        time.sleep(10)
        operation = client.operations.get(operation)

    return client, operation


def return_video(prompt: str) -> bytes:
    """
    Generates the video, saves it temporarily, reads it into a buffer, and returns the buffer.
    Legacy function for backward compatibility.
    """
    if genai is None:
        raise ImportError("google-genai package is required")
        
    client, operation = generate_video_operation(prompt)
    file_path = "temp_dialogue_video.mp4"
    
    # Ensure the operation successfully generated a video
    if not operation.response.generated_videos:
        raise Exception("Video generation failed or returned no video.")

    generated_video = operation.response.generated_videos[0]
    
    # Download and save the file temporarily
    client.files.download(file=generated_video.video)
    generated_video.video.save(file_path)

    # Read the saved file into a binary buffer
    with open(file_path, 'rb') as video_file:
        video_buffer = video_file.read()
    
    # Clean up the temporary local file
    os.remove(file_path)
    
    print(f"Successfully generated and returned video buffer.")
    
    return video_buffer


async def main():
    """Example usage of the VideoAgent."""
    try:
        agent = VideoAgent(api_key=api_key)
        result = await agent.generate_video(
            prompt="two big black men kissing on the lips",
            duration=10,
            quality="high"
        )
        
        if result.video_data:
            filename = agent.save_video(result.video_data, result.filename or "example_video.mp4")
            print(f"Video saved as: {filename}")
            print(f"Duration: {result.duration} seconds")
        else:
            print("No video generated")
        
    except Exception as e:
        print(f"Error in main: {e}")


if __name__ == "__main__":
    # Test with a professional prompt
    asyncio.run(main())
