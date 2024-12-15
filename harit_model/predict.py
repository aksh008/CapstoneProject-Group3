import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))
import chainlit as cl
from openai import OpenAI
import openai
from typing import Union
import pandas as pd
import numpy as np
import json
from harit_model import __version__ as _version
from harit_model.config.core import config
from harit_model.processing.features import preprocess_image
from harit_model.processing.data_manager import load_pipeline
from harit_model.config.core import TRAINED_MODEL_DIR
from harit_model.config.core import INDICES_DIR
import os

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.h5"
plant_diesease_model= load_pipeline(file_name=pipeline_file_name)

test_data = config.app_config.test_data_dir


def make_prediction(img_path):

    # def list_files_in_folder(folder_path):
    #     """
    #     List all files in a folder.

    #     Args:
    #         folder_path (str): Path to the folder.

    #     Returns:
    #         list: List of file names in the folder.
    #     """
    #     try:
    #         file_names = os.listdir(folder_path)
    #         return file_names

    # #load class indices
    
    try:
        with open(INDICES_DIR/"class_indices.json", "r") as json_file:
            class_indices = json.load(json_file)
    except Exception as e:
        print("File not Found")


    class_indices = list(class_indices.keys())

    # files = list_files_in_folder(test_data)
    # img_path = files[0]
    img_array = preprocess_image(img_path)
    predictions = plant_diesease_model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    predicted_label = class_indices[predicted_class[0]]
    print(f"Predicted label: {predicted_label}")
    return predicted_label

api = "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"

# API_KEY = os.getenv("OPENAI_API_KEY")

def get_chatgpt_diagnosis(disease):

    client = OpenAI(
        api_key=api,  # This is the default and can be omitted
    )

    chat_completion = client.chat.completions.create(
       messages=[
                    {
                        "role": "system",
                        "content": "You are an agricultural expert specializing in plant disease treatment. "
                                   "Provide comprehensive, practical treatment recommendations."
                    },
                    {
                        "role": "user",
                        "content": f"Based on this plant disease analysis,please show plant name and Disease name first then  provide detailed treatment recommendations below 200 words : {disease}"
                    }
                ],
        model="gpt-4o-mini",
    )
    return chat_completion
    
    
@cl.on_chat_start
async def start():
    # cl.user_session.set("model", load_model("plant_disease_model.h5"))
    
    await cl.Message(content = "Please upload Image with text").send()


@cl.on_message
async def op(msg: cl.Message):
    # Check if the message contains any files (image input)
    images = [file for file in msg.elements if "image" in file.mime]
    
    if images:  # If images are attached
        img_path = images[0].path
        
        # Display the uploaded image
        # image = cl.Image(path=img_path, name="uploaded_image", display="inline")
        # await cl.Message(
        #     content="Here is the uploaded image:",
        #     elements=[image]  # Attach the image to the message
        # ).send()
        
        # Get the predicted disease from the image
        predicted_disease = make_prediction(img_path)
        
        # Then pass the predicted disease to get_chatgpt_diagnosis
        response = get_chatgpt_diagnosis(predicted_disease)
        
        # Send the response from ChatGPT
        await cl.Message(
            content=f"{response.choices[0].message.content}", 
            author="plantcure"
        ).send()
    
    elif msg.content:  # If only text is provided
        # Directly pass the text to ChatGPT for diagnosis
        response = get_chatgpt_diagnosis(msg.content)
        
        # Send the response from ChatGPT
        await cl.Message(
            content=f"{response.choices[0].message.content}", 
            author="plantcure"
        ).send()
    
    else:
        # If no valid input is provided
        await cl.Message(
            content="Please provide an image or text for processing.",
            author="plantcure"
        ).send()















# if __name__ == "__main__":

#     # Get user input for the image path
#     img_path = input("Enter the path to the image: ").strip()

#     # Validate if the provided path exists
#     if not os.path.exists(img_path):
#         print(f"Error: The file '{img_path}' does not exist. Please check the path and try again.")
#     else:
#         # Make prediction
#         make_prediction(img_path)