from pathlib import Path
import sys

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
# from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers import get
from clearml import Task, OutputModel, InputModel
# from train_pipeline import task

from harit_model.config.core import config

file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

parameters = {
    'epoch': config.model_config.epochs,
    'optimizer': 'Adam',
    'learning_rate':0.001
}

project_name = config.app_config.clearmlconfig.project_name
task = Task.init(project_name=project_name, task_name=f"train_task_{project_name}")

def train_mobilenetv2(num_classes):
    """
    Create and compile the MobileNetV2 model.

    Args:
        num_classes (int): Number of output classes.

    Returns:
        model: Compiled Keras model.
    """
    base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
    base_model.trainable = False  # Freeze base layers 

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    optimizer = get(parameters['optimizer'])
    optimizer.learning_rate = parameters['learning_rate']  # Set learning rate directly
    
    model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model