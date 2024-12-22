from typing import Any, List, Optional
from pydantic import BaseModel
from fastapi import File, UploadFile

# Define a model for predictions
class PredictionResults(BaseModel):
    errors: Optional[Any]
    version: str
    predictions: str  # Or modify this to any other structure depending on your model output


# Define a model for handling image inputs (using file upload)
class ImageDataInputSchema(BaseModel):
    # This can be used to hold any metadata information about the image if required
    # In this case, we're assuming you just need to accept the image file directly
    image: UploadFile  # This expects an image file to be uploaded.

    class Config:
        schema_extra = {
            "example": {
                "image": "example_image_file_path_or_base64_string"  # This is an example, the actual input will be a file.
            }
        }

        
class MultipleImageDataInputs(BaseModel):
    inputs: List[ImageDataInputSchema]  # This handles multiple images

    class Config:
        schema_extra = {
            "example": {
                "inputs": [
                    {
                        "image": "example_image_path_or_base64_string"  # Example image file or base64 string
                    }
                ]
            }
        }

# FastAPI endpoint for image prediction
# from fastapi import FastAPI, UploadFile, File

# app = FastAPI()

# @app.post("/predict_image/")
# async def predict_image(file: UploadFile = File(...)):
#     # Handle the uploaded image file
#     # You could save it or process it in memory depending on your model's requirements
#     contents = await file.read()  # Read the file contents
    
#     # Use this content in your model prediction logic here
    
#     prediction = 1  # Example prediction result, replace with your model's output
    
#     return {"prediction": prediction}
