import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.optimizers import get
from tensorflow.keras.models import load_model
from tensorflow.keras.optimizers import Adam, get
from clearml import InputModel, Model

from harit_model.config.core import TRAINED_MODEL_CHECKPOINT, config

parameters = {
    'epoch': config.model_config.epochs,
    'optimizer': 'Adam',
    'learning_rate': 0.001
}

def train_mobilenetv2(num_classes):
    """
    Create and compile the MobileNetV2 model.

    Args:
        num_classes (int): Number of output classes.

    Returns:
        model: Compiled Keras model.
    """
    base_model = MobileNetV2(input_shape=(224, 224, 3), 
                             include_top=False, 
                             weights='imagenet')
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

# Gets the model id of .keras model
def get_model_id():
    models = Model.query_models(
        project_name=config.app_config.clearmlconfig.project_name,
        tags=["keras"]
    )
    model_id = models[0].id
    return model_id

def retrain_mobilenetv2(task, num_classes):
    """
    Load, configure, and compile the MobileNetV2 model for retraining.
    
    Args:
        num_classes (int): Number of output classes.

    Returns:
        model: Compiled Keras model.
    """
    try:
        input_model = InputModel(model_id=get_model_id())
        task.connect(input_model)

        model_path = TRAINED_MODEL_CHECKPOINT / config.app_config.clearmlconfig.checkpoint_name
        print("path of model picked for retraining ", model_path)
        
        model = load_model(model_path)
        print("Model loaded successfully!")

        task.connect(model)

        optimizer = get(parameters['optimizer'])
        optimizer.learning_rate = parameters['learning_rate']

        model.compile(
            optimizer=optimizer,
            loss="categorical_crossentropy",
            metrics=["accuracy"]
        )

        return model

    except FileNotFoundError as e:
        print(f"Error: Model checkpoint file not found. {str(e)}")
        raise
    except ValueError as e:
        print(f"Error: Issue with loading model or configuring optimizer. {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error occurred: {str(e)}")
        raise