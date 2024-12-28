from pathlib import Path
import sys

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
# from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import get
from clearml import Task, OutputModel, InputModel
from tensorflow.keras.models import load_model
# # # from train_pipeline import task

# # from harit_model.config.core import config

file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

parameters = {
    'epoch': 2,
    # 'neurons': 128,
    # 'hidden_layers':2,
    # 'activation': 'relu',
    'optimizer': 'Adam',
    'learning_rate':0.001
}

task = Task.init(project_name='Harit_project_26Dec',task_name='training_task_26th dec')
def train_mobilenetv2(num_classes):
    """
    Create and compile the MobileNetV2 model.

    Args:
        num_classes (int): Number of output classes.

    Returns:
        model: Compiled Keras model.
    """
    # base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    # base_model.trainable = False  # Freeze base layers  
    # model = Sequential([
    #     base_model,
    #     GlobalAveragePooling2D(),
    #     Dense(256, activation='relu'),
    #     Dense(38, activation='softmax')  # Adjust the number of classes as needed
    #     ])
    input_model = InputModel(model_id="b88b00c23dc54928a2c51b02de26fd38")
    task.connect(input_model)
    model= load_model("trained_models/plant_disease_model_v2.keras")
    print("finally Model loaded successfully!")
    # Save as TensorFlow SavedModel
    # saved_model_dir = "C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.tf"
    # model.save(saved_model_dir, save_format="tf")
    # model= load_model("C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.tf")
    
    # input_model = InputModel(model_id="b88b00c23dc54928a2c51b02de26fd38")
    # local_path = input_model.get_local_copy()
    # print(local_path)
    # ks_model = None
    # try:
    #     # Try to load the model as a full Keras model
    #     model.load_weights(local_path)
    #     print("Weights loaded successfully!")
    # except Exception as e:
    #     print(f"Could not load full model: {e}")
    #     print("Loading weights and rebuilding architecture.")
    task.connect(model)
    # model = Sequential([
    #     ks_model,
    #     GlobalAveragePooling2D(),
    #     Dense(256, activation='relu'),
    #     Dense(num_classes, activation='softmax')
    # ])
    optimizer = get(parameters['optimizer'])
    optimizer.learning_rate = parameters['learning_rate']  # Set learning rate directly
    
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model

# if __name__ == "__main__":

#     base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
#     base_model.trainable = False  # Freeze base layers

# model = Sequential([
#     base_model,
#     GlobalAveragePooling2D(),
#     Dense(256, activation='relu'),
#     Dense(38, activation='softmax')  # Adjust the number of classes
# ])
# import os
# import h5py
# print(os.path.exists("C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.h5"))

# # Load weights
# try:
#     with h5py.File("C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.h5", 'r') as file:
#         print("File is a valid HDF5 file.")
#     # model.load_weights("C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.h5")
#     # print("Weights loaded successfully!")
#     model= load_model("C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.h5")
#     # Save as TensorFlow SavedModel
#     saved_model_dir = "C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.keras"
#     model.save(saved_model_dir)
#     # model= load_model("C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.tf")
#     reloaded_model = tf.keras.models.load_model(saved_model_dir)
#     # model= load_model("C:/Akshay/AIMLOps24/Capstone Project/akshay_25dec/CapstoneProject-Group3/harit_model/trained_models/plant_disease_model_v2.h5")
#     print("finally Model loaded successfully!")
# # except Exception as e:
# #     print(f"Could not load weights: {e}")