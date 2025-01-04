from pathlib import Path
import sys
import os
file = Path(__file__).resolve()
root = file.parents[2]
print("root is", root)
sys.path.append(str(root))
# print("sys path is", sys.path)
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from pathlib import Path
import chainlit as cl
from openai import OpenAI
from literalai import LiteralClient
from harit_model.predict import make_prediction
from chainlit.utils import mount_chainlit
# from prometheus_fastapi_instrumentator import Instrumentator
import base64
from dotenv import load_dotenv
from typing import Optional
from fastapi import FastAPI
import uvicorn
import ssl
from pathlib import Path
from core import load_languages

# Config and Initialization
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key not found")

client = OpenAI(api_key=OPENAI_API_KEY)
literalai_client = LiteralClient(api_key=os.getenv("LITERAL_API_KEY"))
literalai_client.instrument_openai()

app = FastAPI(title="Plant Disease Detection API")
api_router = APIRouter()

SYSTEM_PROMPT = """You are a plant disease detection assistant. Your role:
- Respond to "Hi" or "Hello" with: "Hello! Please upload a plant leaf image you would like me to analyze."
- Ask users to upload the plant image.
- Analyze plant diseases and provide treatment.
- Give accurate identifications with confidence levels.
- Suggest practical treatment options.
- Maintain a helpful tone.
- Include safety warnings."""

app.include_router(api_router)
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application with Prometheus monitoring! Go to /chainlit for the chatbot UI."}
# Helper Functions
def is_valid_leaf(file_content) -> bool:
    try:
        base64_image = base64.b64encode(file_content.read()).decode("utf-8")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Is this a plant/leaf image? Answer LEAF or NOT_LEAF."},
                {"role": "user", "content": f"data:image/jpeg;base64,{base64_image}"}
            ]
        )
        print("Response from OpenAI:", response)  # Debug response
        if "choices" in response and response.choices:
            return "LEAF" in response.choices[0].message.content.upper()
        return False
    except Exception as e:
        print(f"Image validation error: {str(e)}")
        return False


@literalai_client.step(type="run")
def get_disease_analysis(disease: str, language: str) -> str:
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Analyze this plant disease and provide treatment below 200 words in {language}: {disease}"}
            ],
            model="gpt-4o-mini"
        )
        print("Response from OpenAI:", response)  # Debug response
        if "choices" in response and response.choices:
            return response.choices[0].message.content
        return "No response available"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Chainlit Handlers
@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome to Harit Bot Plant Disease Detection!", author="plantcure").send()
    await cl.Message(content="I can detect diseases for Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soybean, and Tomato").send()
    languages = load_languages()
    # languages = ["English", "Hindi", "Spanish"]  # Add more languages as needed
    actions = [cl.Action(name=lang, value=lang, label=lang) for lang in languages]
    language = await cl.AskActionMessage(content="Select language:", actions=actions).send()
    print(language.get("value"))
    cl.user_session.set("language", language.get("value"))

@cl.on_message
async def process_message(msg: cl.Message):
    try:
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
                    content="uploaded image:", elements=[image_display]
                ).send()
                if isValidLeaf:
                    results = make_prediction(image.path)
                    plant_name, disease_name = results.split("___")
                    is_healthy = disease_name.lower() == "healthy"
                    if is_healthy:
                        await cl.Message(
                            content=f"Plant name : {plant_name} and Plant leaf is healthy",
                            author="plantcure",
                        ).send()
                    else:
                        language_preference = cl.user_session.get("language", "English")
                        response = get_disease_analysis(results, language_preference)
                        await cl.Message(
                            content=f"{response.choices[0].message.content}",
                            author="plantcure"
                        ).send()
                else:
                    await cl.Message(
                        content="Please provide a valid leaf or a plant image!", 
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
                response = get_disease_analysis(msg.content, language_preference)
            await cl.Message(
                content=f"{response}",
                author="plantcure"
            ).send()
            return
    except Exception as e:
        await cl.Message(content=f"Error: {str(e)}", author="plantcure").send()
    return



def start_chainlit():
    mount_chainlit(app, target=__file__, path="/chainlit")

@app.get("/supported-plants")
def supported_plants():
    plants = [
        "Apple", "Blueberry", "Cherry", "Corn", "Grape", "Orange",
        "Peach", "Pepper", "Potato", "Raspberry", "Soybean", "Tomato"
    ]
    return {"message": "Here is a list of plants we currently support:", "supported_plants": plants}

def configure_ssl():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
    try:
        ssl_context.load_cert_chain(
            r'C:\Akshay\AIMLOps24\Capstone Project\main-3jan\CapstoneProject-Group3\harit_model_api\app\Cert\cert.pem',
            r'C:\Akshay\AIMLOps24\Capstone Project\main-3jan\CapstoneProject-Group3\harit_model_api\app\Cert\key.pem'
        )
        print("SSL Certificate and Key loaded successfully.")
    except Exception as e:
        print(f"Failed to load SSL Certificate/Key: {e}")
    return ssl_context

if __name__ == "__main__":
    start_chainlit()
    ssl_context = configure_ssl()
    print("SSL context successfully created")
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8443,
        ssl_context=ssl_context,
        ssl_certfile=r"C:\\Akshay\\AIMLOps24\\Capstone Project\\main-3jan\\CapstoneProject-Group3\\harit_model_api\\app\\Cert\\cert.pem",
        ssl_keyfile=r"C:\\Akshay\\AIMLOps24\\Capstone Project\\main-3jan\\CapstoneProject-Group3\\harit_model_api\\app\\Cert\\key.pem",
        ssl_version=ssl.PROTOCOL_TLS_SERVER,
        ssl_cert_reqs=ssl.CERT_REQUIRED,
        workers=4,
        # log_level=debug
    )