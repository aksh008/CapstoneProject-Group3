import base64
from gettext import translation
import os
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException, APIRouter
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import chainlit as cl
from openai import OpenAI
from literalai import LiteralClient
from harit_model.predict import make_prediction
from chainlit.utils import mount_chainlit
from prometheus_fastapi_instrumentator import Instrumentator
from core import load_languages, translations, language_mapping

####################################PROMETHEUS RELATED LIBRARY IMPORT######################################
from prometheus_client import Gauge, Counter, Histogram, CollectorRegistry, REGISTRY
import psutils
from fastapi import FastAPI, Request
import time
###########################################################################################################


# Load environment variables
load_dotenv()
SYSTEM_PROMPT = """You are a plant disease detection assistant. Your role:
- Ask users to upload the plant image.
- Once you get {Plant_Name} and {disease_name}, must Analyze plant diseases and provide treatment and provide all information to user.
- you can detect disease only for these plant: Apple, Blueberry, Cherry, Corn, Grape, Orange, Peach, Pepper, Potato, Raspberry, Soyabean, Strawberry, Squash and Tomato
- You Must politely deny the user in case user ask for detecting disease for any other plants.
- Give accurate identifications with confidence levels.
- Suggest practical treatment options.
- Maintain a helpful tone.
- Include safety warnings."""

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


#############################PROMETHEUS CODE START######################################################

total_latency = 0.0
request_count = 0
# Helper function to get or create metrics
def get_or_create_metric(metric_type, name, description, labelnames=None):
    if name in REGISTRY._names_to_collectors:
        collector = REGISTRY._names_to_collectors[name]
        if metric_type == "gauge" and isinstance(collector, Gauge):
            return collector
        elif metric_type == "counter" and isinstance(collector, Counter):
            return collector
        elif metric_type == "histogram" and isinstance(collector, Histogram):
            return collector
        else:
            raise ValueError(f"Metric '{name}' already exists and is not a '{metric_type}'.")
    else:
        if metric_type == "gauge":
            return Gauge(name, description)
        elif metric_type == "counter":
            return Counter(name, description, labelnames=labelnames or [])
        elif metric_type == "histogram":
            return Histogram(name, description, labelnames=labelnames or [])
        else:
            raise ValueError(f"Unknown metric type: {metric_type}")

# Define Prometheus metrics
CPU_USAGE = get_or_create_metric("gauge", "cpu_usage_percent", "CPU usage in percentage")
MEMORY_USAGE = get_or_create_metric("gauge", "memory_usage_bytes", "Memory usage in bytes")
HTTP_REQUEST_COUNT = get_or_create_metric(
    "counter",
    "http_request_count",
    "Number of HTTP requests",
    labelnames=["method", "endpoint"]
)
HTTP_REQUEST_COUNT_TOTAL_HARIT = get_or_create_metric(
    "counter",
    "http_request_count_total_harit",
    "Total number of HTTP requests (including default and /chainlit)",
)
AVERAGE_LATENCY = get_or_create_metric(
    "gauge",
    "average_request_latency_seconds",
    "Average latency of HTTP requests in seconds"
)
CONCURRENT_REQUESTS = get_or_create_metric(
    "gauge",
    "concurrent_requests",
    "Number of concurrent requests being processed"
)

# Function to update system metrics
def update_system_metrics():
    # Track CPU usage of only this FastAPI process
    process = psutil.Process(os.getpid())
    
     # To ensure a more accurate reading, get CPU usage and store it
    cpu_usage = process.cpu_percent(interval=None)  # A shorter interval will allow better real-time tracking
    
    # Set the CPU usage metric with more accurate and real-time data
    CPU_USAGE.set(cpu_usage)
    # Use only memory utilized by the current FastAPI process
    MEMORY_USAGE.set(process.memory_info().rss / (1024 ** 3))  # Convert to GB


# Middleware to track latency and request count
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    global total_latency, request_count

    # Exclude `/metrics` endpoint from tracking
    if request.url.path == "/metrics":
        return await call_next(request)

    # Track requests to `/` and `/chainlit`
    if request.url.path == "/" or request.url.path.startswith("/chainlit"):
        HTTP_REQUEST_COUNT_TOTAL_HARIT.inc()

    # Increment concurrent requests
    CONCURRENT_REQUESTS.inc()

    try:
        # Track start time for latency calculation
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time

        # Update Prometheus metrics
        HTTP_REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()  # Total requests
        total_latency += process_time
        request_count += 1

        # Calculate and set average latency
        AVERAGE_LATENCY.set(total_latency / request_count if request_count > 0 else 0)

        return response
    finally:
        # Ensure concurrent requests are never less than 1 if any request has been made
        if CONCURRENT_REQUESTS._value.get() > 1:
            CONCURRENT_REQUESTS.dec()
        elif CONCURRENT_REQUESTS._value.get() == 1:
            # Do not decrement to 0 for single active request
            pass


#############################PROMETHEUS CODE END########################################################

def get_translated_message(key, language, *args):
    if language not in language_mapping:
        language = "English"  # Default to English if language not found
    message = translations[language].get(key, translations["English"][key])
    return message.format(*args) if args else message

app.include_router(api_router)
# Add a default route
Instrumentator().instrument(app).expose(app, endpoint="/metrics")
@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI application with Prometheus monitoring! Go to /chainlit for the chatbot UI."}

# Chainlit integration

@literalai_client.step(type="run")
def get_chatgpt_diagnosis(disease, language):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Based on this plant disease analysis, please show plant name and Disease name first then provide detailed treatment recommendations below 200 words in {language}: {disease}",
            },
        ],
        model="gpt-4o-mini",
    )
    return response

@literalai_client.step(type="run")
def get_chatgpt_text_response(text, language):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": f"Respond to the user query {text} in {language} in 200 words or less",
            },
        ],
        model="gpt-4o-mini",
    )
    return response

language = None

@cl.on_chat_start
async def start():
    languages = load_languages()
    actions = [
        cl.Action(
            name=lang,
            value=lang,
            label=language_mapping.get(lang, lang)  # Use native name if available, otherwise use English name
        )
        for lang in languages
    ]
    
    language = await cl.AskActionMessage(
        content="Please select language!",
        actions=actions,
    ).send()
    if language is not None:
        cl.user_session.set("language", language.get("value"))
    
    current_language = cl.user_session.get("language", "en")
    await cl.Message(
        content= get_translated_message("welcome", current_language), 
        author="plantcure",
    ).send()


@cl.on_message
async def process_message(msg: cl.Message):
    allowed_image_extensions = [".jpg", ".jpeg", ".png", ".heic", ".heif"]
    valid_images = []
    plain_text = None
    current_language = cl.user_session.get("language", "en")

    for element in msg.elements:
        if hasattr(element, "name"):
            extension = os.path.splitext(element.name)[1].lower()
            if extension in allowed_image_extensions:
                valid_images.append(element)
            else:
                await cl.Message(
                    content= get_translated_message("unsupported_file", current_language, extension, extension), 
                    author="plantcure",
                ).send()
                return

    if msg.content:
        plain_text = msg.content.strip()

    if not valid_images and not plain_text:
        await cl.Message(
            content= get_translated_message("invalid_input", current_language), 
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
            file_content.close()

            image_display = cl.Image(
                path=image.path, name="uploaded_image", display="inline"
            )
            results = make_prediction(image.path)
            plant_name, disease_name = results.split("___")
            print("plant name: ", plant_name)
            print("disease_name :", disease_name)

            if(plant_name == "RandomImage"):
                isValidLeaf = False
                
            await cl.Message(
                content= get_translated_message("uploaded_image", current_language), 
                elements=[image_display]
            ).send()
            
            if isValidLeaf == True:                
                is_healthy = disease_name.lower() == "healthy"
                if is_healthy:
                    await cl.Message(
                        content= get_translated_message("healthy_plant", current_language, plant_name), 
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
                    content= get_translated_message("provide_valid_image", current_language), 
                    author="plantcure"
                ).send()

        except Exception as e:
            await cl.Message(
                content= get_translated_message("error_processing", current_language, str(e)), 
                author="plantcure"
            ).send()
        return

    if not valid_images and plain_text:
        with literalai_client.thread(name="Example"):
           language_preference = cl.user_session.get("language", "English")
           response = get_chatgpt_text_response(msg.content, language_preference)
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
