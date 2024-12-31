import base64
import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import chainlit as cl
from openai import OpenAI
from literalai import LiteralClient
from harit_model.predict import make_prediction
# from api import api_router
# from harit_model_api.app import __version__, schemas
# from api import predict
from chainlit.utils import mount_chainlit
from prometheus_fastapi_instrumentator import Instrumentator

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)
literalai_client = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
literalai_client.instrument_openai()

# FastAPI app initialization
app = FastAPI()
api_router = APIRouter()

app.include_router(api_router)
# Add a default route
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application with Prometheus monitoring! Go to /chainlit for the chatbot UI."}

# Chainlit integration
@literalai_client.step(type="run")
def is_valid_leaf(image_content):
    prompt = "Check if the image is a plant or a leaf image. The answer should be either LEAF or NOT_LEAF."
    base64_image = base64.b64encode(image_content.read()).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=300,
        )
        result = response.choices[0].message.content.strip().upper()
        return "LEAF" in result and "NOT" not in result
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

@literalai_client.step(type="run")
def get_chatgpt_diagnosis(disease, language):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an agricultural expert specializing in plant disease treatment. Provide comprehensive, practical treatment recommendations.",
            },
            {
                "role": "user",
                "content": f"Based on this plant disease analysis, please show plant name and Disease name first then provide detailed treatment recommendations below 200 words in {language}: {disease}",
            },
        ],
        model="gpt-4o-mini",
    )
    return response


language = None

@cl.on_chat_start
async def start():
    await cl.Message(
        content="Welcome To Harit Bot ",
        author="plantcure",
    ).send()

    # language = await cl.AskUserMessage(content="What is your language?", timeout=90).send()
    # language = language.get('output', '')
    # cl.user_session.set("language", language)
    # if language:
    #     await cl.Message(
    #         content=f"Your language is: {language}, now give input",
    #     ).send()

@cl.on_message
async def process_message(msg: cl.Message):
    allowed_image_extensions = [".jpg", ".jpeg", ".png", ".heic", ".heif"]
    valid_images = []
    plain_text = None

    for element in msg.elements:
        if hasattr(element, "name"):
            extension = os.path.splitext(element.name)[1].lower()
            if extension in allowed_image_extensions:
                valid_images.append(element)
            else:
                await cl.Message(
                    content=f"Unsupported file type: {extension}. Only Images with .jpg, .jpeg, .png, .heic is allowed",
                    author="plantcure",
                ).send()
                return

    if msg.content:
        plain_text = msg.content.strip()

    if not valid_images and not plain_text:
        await cl.Message(
            content="Invalid input. Please upload an image file or provide text input.",
            author="plantcure",
        ).send()
        return

    isValidLeaf = True
    if valid_images:
        image = valid_images[0]
        try:
            file_content = open(image.path, "rb")
            upload_file = UploadFile(
                filename=os.path.basename(image.path), file=file_content
            )
            isValidLeaf = is_valid_leaf(file_content)
            file_content.close()

            image_display = cl.Image(
                path=image.path, name="uploaded_image", display="inline"
            )

            await cl.Message(
                content="Here is the uploaded image:", elements=[image_display]
            ).send()
            if isValidLeaf == True:
                results = make_prediction(image.path)
                plant_name, disease_name = results.split("___")
                is_healthy = disease_name.lower() == "healthy"
                if is_healthy:
                    await cl.Message(
                        content=f"Plant name : {plant_name} and Plant leafs are healthy",
                        author="plantcure",
                    ).send()
                else:
                    language_preference = cl.user_session.get("language", "English")
                    response = get_chatgpt_diagnosis(results, language_preference)
                    await cl.Message(
                        content=f"{response.choices[0].message.content}", 
                        author="plantcure"
                    ).send()
            else:
                await cl.Message(
                    content="Please add a valid leaf or a plant image!", 
                    author="plantcure"
                ).send()

        except Exception as e:
            await cl.Message(
                content=f"An error occurred during image processing: {str(e)}",
                author="plantcure"
            ).send()
        return

    if plain_text:
        with literalai_client.thread(name="Example"):
           language_preference = cl.user_session.get("language", "English")
           response = get_chatgpt_diagnosis(msg.content, language_preference)
        await cl.Message(
            content=f"{response.choices[0].message.content}",
            author="plantcure"
        ).send()
        return

# Mount Chainlit into FastAPI
def start_chainlit():
    mount_chainlit(app, target=__file__, path="/chainlit")

if __name__ == "__main__":
    import uvicorn
    start_chainlit()
    uvicorn.run(app, host="0.0.0.0", port=8000)
