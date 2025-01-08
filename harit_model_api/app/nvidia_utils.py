import base64
import io
import json
import logging
from collections import deque
from datetime import datetime, timedelta
from typing import Optional

import requests
from PIL import Image
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()  # Load environment variables from .env

# Custom exceptions
class APIError(Exception):
    """Custom exception for API-related errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        super().__init__(message)
        self.status_code = status_code

class JSONParseError(Exception):
    """Custom exception for JSON parsing errors."""
    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        super().__init__(message)
        self.original_exception = original_exception

# Module-level variables for rate limiting
_requests_queue = deque()
_max_requests = 10
_time_window = 60
_model = None
_nvidia_headers = None

def _check_rate_limit() -> bool:
    """Check if the request can proceed based on rate limiting."""
    now = datetime.now()
    while _requests_queue and _requests_queue[0] < now - \
            timedelta(seconds=_time_window):
        _requests_queue.popleft()
    if len(_requests_queue) < _max_requests:
        _requests_queue.append(now)
        return True
    return False

def _init_nvidia_api() -> None:
    """Initialize the Nvidia API with configuration."""
    global _nvidia_headers

    if _nvidia_headers is not None:
        return

    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        logger.error("NVIDIA_API_KEY environment variable not set")
        raise ValueError("NVIDIA_API_KEY environment variable not set")

    try:
        _nvidia_headers = {
            "Authorization": f"Bearer {api_key}",
            "Accept": "application/json"
        }

        logger.info("API initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize API: {str(e)}")
        raise

def chat_with_nvidia(prompt):

    payload = {
        "messages": [
        {
            "role": "user",
            "content": prompt
        }
        ],
    "max_tokens": 1024,
    "temperature": 0.50,
    "top_p": 0.70,
    "seed": 0,
    "stream": False
    }

    neva_api_url = "https://ai.api.nvidia.com/v1/vlm/nvidia/neva-22b"

    response = requests.post(neva_api_url, headers=_nvidia_headers, json=payload)
    response = response.json()

    return response["choices"][0]["message"]["content"]

def _get_image_classification(image: object) -> object:

    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    image = buf.getvalue()
    image_b64 = base64.b64encode(image).decode()
    assert len(image_b64) < 180_000, "Image to large to upload."

    prompt = f'''You are an expert plant leaf image classifier, who can classify if the given image contains a plant leaf.
        Respond in a structured JSON format that can be directly parsed into a Python dictionary/object. 
        The structure should be as follows:

        {{"isLeaf": "set to true if it is a plant leaf. else false.",
        "class": "what type of object it is"
        }} '''

    prompt = prompt + f'<img src="data:image/jpeg;base64,{image_b64}" />'

    response = chat_with_nvidia(prompt)

    return response

def get_plant_image_details(image_file: Image.Image) -> bool:
    """
    Retrieves plant disease details using the Nvidia API

    Args:
        Image_file (Image.Image):Image file to identify if it belongs to leaf class

    Returns:
        Classifier: True if it is a leaf image, false otherwise

    Raises:
        ValueError: If image name is invalid
        APIError: If API request fails or rate limit is exceeded
        JSONParseError: If response parsing fails
    """
    if not image_file:
        logger.error("Invalid image provided")
        raise ValueError("Image should be non-empty")

    if not _check_rate_limit():
        logger.warning("Rate limit exceeded")
        raise APIError("Rate limit exceeded. Please try again later.")

    try:
        # Initialize API if not already done
        _init_nvidia_api()

        logger.info("Validating image for leaves")

        response = _get_image_classification(image_file)
        #print("response form method_get_image_classifiction",response)

        if not response:
            logger.error("Empty response from API")
            raise APIError("Received empty response from API")

        try:
            # Parse the JSON response into a Python dictionary
            json_response = response
            parsed_response = json.loads(s = json_response)

            #print("Parsed response", parsed_response)

            # Check the classification result
            is_leaf = parsed_response["isLeaf"]
            logger.info(f"Successfully verified image for leaves {is_leaf}")

            return is_leaf

        except json.JSONDecodeError as e:
            logger.error(f"JSON Decode Error: {str(e)}")
            raise JSONParseError(f"Failed to parse API response: {str(e)}")

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise APIError(f"Error processing request: {str(e)}")

def configure_rate_limit(
        max_requests: int = 10,
        time_window: int = 60) -> None:
    """
    Configure rate limiting parameters.

    Args:
        max_requests (int): Maximum number of requests allowed in the time window
        time_window (int): Time window in seconds
    """
    global _max_requests, _time_window
    _max_requests = max_requests
    _time_window = time_window

configure_rate_limit(max_requests=10, time_window=60)


if __name__ == "__main__":
    # Load an image using Pillow
    #image_path = "/Users/hemanth/Downloads/ICICI-Chequ.jpg"
    image_path = "/Users/hemanth/Downloads/book.jpg"
    #image_path = "/Users/hemanth/Downloads/Holdings.csv"
    #image_path = "/Users/hemanth/Downloads/table.jpg"
    #image_path = "/Users/hemanth/Downloads/straw1.jpg"
    #image_path = "/Users/hemanth/Downloads/tree1.jpg"
    #image_path = "/Users/hemanth/Documents/AI/IISC/AI-ML-Classes/CapstoneProject-Group3/harit_model/dataset/New Plant Diseases Dataset(Augmented)/New Plant Diseases Dataset(Augmented)/valid/Apple___healthy/0a02e8cb-b715-497f-a16a-c28b3409f927___RS_HL 7432.JPG"
  
  # Validate file extension
    valid_extensions = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff')
    if not image_path.lower().endswith(valid_extensions):
        #raise ValueError(f"Invalid file type: {image_path}. Please provide an image file.")
        print("invalid format") 
    else:
        image = Image.open(image_path)
        print(get_plant_image_details(image))