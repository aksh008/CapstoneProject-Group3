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
    'epoch': 2,
    # 'neurons': 128,
    # 'hidden_layers':2,
    # 'activation': 'relu',
    'optimizer': 'Adam',
    'learning_rate':0.001
}

task = Task.init(project_name='Harit_project_25Dec',task_name='training_task_25th dec')
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

    # input_model = InputModel(model_id="b88b00c23dc54928a2c51b02de26fd38")
    # task.connect(input_model)

    input_model = InputModel(model_id="b88b00c23dc54928a2c51b02de26fd38")
    local_path = input_model.get_local_copy()
    ks_model = None
    try:
        # Try to load the model as a full Keras model
        ks_model = tf.keras.models.load_model(local_path)
    except Exception as e:
        print(f"Could not load full model: {e}")
        print("Loading weights and rebuilding architecture.")
    task.connect(ks_model)
    # model = Sequential([
    #     ks_model,
    #     GlobalAveragePooling2D(),
    #     Dense(256, activation='relu'),
    #     Dense(num_classes, activation='softmax')
    # ])
    optimizer = get(parameters['optimizer'])
    optimizer.learning_rate = parameters['learning_rate']  # Set learning rate directly
    
    ks_model.compile(
        optimizer=optimizer,
        loss="categorical_crossentropy",
        metrics=["accuracy"]
    )

    return ks_model