# import sys
# from pathlib import Path
# file = Path(__file__).resolve()
# parent, root = file.parent, file.parents[1]
# sys.path.append(str(root))
# # print(sys.path)
# # from typing import Any

# # from fastapi import APIRouter, FastAPI, Request
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import HTMLResponse

# # from app.api import api_router
# # from app.config import settings
# import openai
# import os
# from openai import OpenAI

# import chainlit as cl
# import kagglehub
# import mimetypes
# from dotenv import load_dotenv
# from literalai import LiteralClient
# from harit_model_api.app.api import predict
# from fastapi import UploadFile
# import shutil


# # Load environment variables
# load_dotenv()



# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
# if not OPENAI_API_KEY:
#     raise ValueError("OpenAI API key not found in environment variables")

# # Initialize OpenAI client
# client = OpenAI(api_key=OPENAI_API_KEY)
# literalai_client = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
# literalai_client.instrument_openai()
# import requests

# response = requests.get('https://cloud.getliteral.ai/api/graphql', timeout=30)
# # openai_client = OpenAI(api_key=OPENAI_API_KEY)
# @literalai_client.step(type="run")
# def get_chatgpt_diagnosis(disease):

#     # client = OpenAI(
#     #     api_key=OPENAI_API_KEY,  # This is the default and can be omitted
#     # )

#     response  = client.chat.completions.create(
#        messages=[
#                     {
#                         "role": "system",
#                         "content": "You are an agricultural expert specializing in plant disease treatment. "
#                                    "Provide comprehensive, practical treatment recommendations."
#                     },
#                     {
#                         "role": "user",
#                         "content": f"Based on this plant disease analysis,please show plant name and Disease name first then  provide detailed treatment recommendations below 200 words : {disease}"
#                     }
#                 ],
#         model="gpt-4o-mini",
#         # max_tokens=300
#     )
#     return response 

# import httpx



# # URL for the /predict endpoint
# # PREDICT_URL = "http://localhost:8001/api/v1/predict"


# @cl.on_chat_start
# async def start():
#     await cl.Message(content="Welcome to PlantCure! Please upload an image of a plant with text", author="plantcure").send()

# @cl.on_message
# async def process_message(msg: cl.Message):
#     allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.heif']
#     valid_images = []
#     plain_text = None

#     for element in msg.elements:
#         if hasattr(element, 'name'):
#             extension = os.path.splitext(element.name)[1].lower()
#             if extension in allowed_image_extensions:
#                 valid_images.append(element)
#             else:
#                 await cl.Message(
#                     content=f"Unsupported file type: {extension}. Only Images with .jpg, .jpeg, .png, .heic is allowed",
#                     author="plantcure"
#                 ).send()
#                 return

#     if msg.content:
#         plain_text = msg.content.strip()

#     if not valid_images and not plain_text:
#         await cl.Message(
#             content="Invalid input. Please upload an image file or provide text input.",
#             author="plantcure"
#         ).send()
#         return

#     if valid_images:
#         image = valid_images[0]
#         try:
#             # Create a FastAPI UploadFile from the Chainlit file
            
            
#             # Create an UploadFile object
#             file_content = open(image.path, 'rb')
#             upload_file = UploadFile(
#                 filename=os.path.basename(image.path),
#                 file=file_content
#             )
            
#             # Display the uploaded image
#             image_display = cl.Image(path=image.path, name="uploaded_image", display="inline")
#             await cl.Message(
#                 content="Here is the uploaded image:",
#                 elements=[image_display]
#             ).send()
#                         # Make a request to the /predict endpoint
#             # with open(image.path, "rb") as file:
#             #     files = {"input_data": (image.name, file)}
#             #     async with httpx.AsyncClient() as client:
#             #         response = await client.post(PREDICT_URL, files=files)


#             # # Predict using the UploadFile object
#             # if response.status_code != 200:
#             #     await cl.Message(
#             #         content=f"Error in prediction: {response.json().get('detail', 'Unknown error')}",
#             #         author="plantcure"
#             #     ).send()
#             #     return

#             prediction_result = await predict(upload_file)
                
#             # response = get_chatgpt_diagnosis(prediction_result.predictions)

#             await cl.Message(
#                 # content=f"{response.choices[0].message.content}",
#                 content=f"{prediction_result}",
#                 author="plantcure"
#             ).send()
            
#             # Close the file
#             file_content.close()

#         except Exception as e:
#             await cl.Message(
#                 content=f"An error occurred during image processing: {str(e)}",
#                 author="plantcure"
#             ).send()
#         return

#     if plain_text:
#         with literalai_client.thread(name="Example") as thread:
#             response = get_chatgpt_diagnosis(msg.content)
#         await cl.Message(
#             content=f"{response.choices[0].message.content}",
#             author="plantcure"
#         ).send()
#         return