import sys
from pathlib import Path
# import matplotlib.pyplot as plt
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import tensorflow as tf
import os
from harit_model.processing.features import train_test_valid
from harit_model.processing.validation import evaluate_model
from harit_model.config.core import config
from harit_model.processing.data_manager import load_dataset, save_pipeline
# from tensorflow.keras.optimizers import Adam

from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from clearml import Task, TaskTypes

task = Task.init(project_name='Harit_project_15Dec',task_name='training_task_1')

parameters = {
    'epoch': 2,
    # 'neurons': 128,
    # 'hidden_layers':2,
    # 'activation': 'relu',
    'optimizer': 'Adam',
    'learning_rate':0.001
}

task.connect(parameters)

def train_mobilenetv2(num_classes):
    """
    Train the MobileNetV2 model on the dataset.

    Args:
        train_data: Training data generator.
        valid_data: Validation data generator.
        epochs (int): Number of epochs for training.
        output_dir (str): Directory to save the trained model.

    Returns:
        model: Trained Keras model.
    """

    

   

    # Load the MobileNetV2 model
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze base layers  
    model = Sequential([
                    base_model,
                    GlobalAveragePooling2D(),
                    Dense(256, activation='relu'),
                    Dense(num_classes, activation='softmax')  # `num_classes` is the number of plant disease categories
                    ])

    # Compile the model
    model.compile(optimizer=parameters['optimizer'](learning_rate=parameters['learning_rate']),
                  loss="categorical_crossentropy",
                  metrics=["accuracy"])

    
    


    return model
