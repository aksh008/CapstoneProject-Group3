import os
from pathlib import Path
import chainlit as cl
from openai import OpenAI
from dotenv import load_dotenv
from literalai import LiteralClient
from fastapi import UploadFile
import shutil
from harit_model.predict import make_prediction

# Load environment variables
load_dotenv()

UPLOAD_DIR = Path("./uploads")
UPLOAD_DIR.mkdir(exist_ok=True)  # Create directory if it doesn't exist

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
literalai_client = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
literalai_client.instrument_openai()

@literalai_client.step(type="run")
def get_chatgpt_diagnosis(disease):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an agricultural expert specializing in plant disease treatment. "
                           "Provide comprehensive, practical treatment recommendations."
            },
            {
                "role": "user",
                "content": f"Based on this plant disease analysis, please show plant name and Disease name first then provide detailed treatment recommendations below 200 words : {disease}"
            }
        ],
        model="gpt-4o-mini",
    )
    return response 

@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome to PlantCure! Please upload an image of a plant with text", author="plantcure").send()

@cl.on_message
async def process_message(msg: cl.Message):
    allowed_image_extensions = ['.jpg', '.jpeg', '.png', '.heic', '.heif']
    valid_images = []
    plain_text = None

    for element in msg.elements:
        if hasattr(element, 'name'):
            extension = os.path.splitext(element.name)[1].lower()
            if extension in allowed_image_extensions:
                valid_images.append(element)
            else:
                await cl.Message(
                    content=f"Unsupported file type: {extension}. Only Images with .jpg, .jpeg, .png, .heic is allowed",
                    author="plantcure"
                ).send()
                return

    if msg.content:
        plain_text = msg.content.strip()

    if not valid_images and not plain_text:
        await cl.Message(
            content="Invalid input. Please upload an image file or provide text input.",
            author="plantcure"
        ).send()
        return

    if valid_images:
        image = valid_images[0]
        try:
            file_content = open(image.path, 'rb')
            upload_file = UploadFile(
                filename=os.path.basename(image.path),
                file=file_content
            )
            
            image_display = cl.Image(path=image.path, name="uploaded_image", display="inline")
            await cl.Message(
                content="Here is the uploaded image:",
                elements=[image_display]
            ).send()
            
            file_path = UPLOAD_DIR / upload_file.filename
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file_content, buffer)
                
            results = make_prediction(file_path)
            plant_name, disease_name = results.split('___')
            is_healthy = disease_name.lower() == 'healthy'
            if is_healthy:
                await cl.Message(
                content=f"Plant name : {plant_name} and Plant leafs are healthy",
                author="plantcure"
                ).send()
            else:
                response = get_chatgpt_diagnosis(results)
                await cl.Message(
                    content=f"{response.choices[0].message.content}",
                    author="plantcure"
                ).send()
                
            file_content.close()

        except Exception as e:
            await cl.Message(
                content=f"An error occurred during image processing: {str(e)}",
                author="plantcure"
            ).send()
        return

    if plain_text:
        with literalai_client.thread(name="Example"):
            response = get_chatgpt_diagnosis(msg.content)
        await cl.Message(
            content=f"{response.choices[0].message.content}",
            author="plantcure"
        ).send()
        return