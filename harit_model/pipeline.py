from pathlib import Path
import sys

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import Adam

from harit_model.config.core import config

file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

def train_mobilenetv2(num_classes):
    """
    Create and compile the MobileNetV2 model.

    Args:
        num_classes (int): Number of output classes.

    Returns:
        model: Compiled Keras model.
    """
    try:
        base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights='imagenet')
        base_model.trainable = False  # Freeze base layers  
    except Exception as e:
        print(f"Error loading MobileNetV2 weights: {e}")
        print("Attempting to use model without pre-trained weights...")
        base_model = MobileNetV2(input_shape=(224, 224, 3), include_top=False, weights=None)
        base_model.trainable = False  # Freeze base layers  

    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model