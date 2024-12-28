import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tensorflow as tf
import numpy as np
import json

from tensorflow.keras.preprocessing.image import load_img, img_to_array, ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

from harit_model.config.core import INDICES_DIR

def preprocess_image(img_path, target_size=(224, 224)):
    print(f"Processing image: {img_path}")
    img = load_img(img_path, target_size=target_size)
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    print("Image preprocessing complete")
    return img_array

def train_test_valid(data_dir, target_size=(224, 224), batch_size=64):
    train_datagen = ImageDataGenerator(rescale=1/255., validation_split=0.2)
    test_datagen = ImageDataGenerator(rescale=1/255.)

    image_shape = target_size

    print("Loading Training Images:")
    train_data = train_datagen.flow_from_directory(
        f"{data_dir}train/",
        target_size=image_shape,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=True,
        subset='training'
    )

    print("Loading Validation Images:")
    valid_data = train_datagen.flow_from_directory(
        f"{data_dir}train/",
        target_size=image_shape,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False,
        subset='validation'
    )

    print('Loading Test Images:')
    test_data = test_datagen.flow_from_directory(
        f"{data_dir}valid/",
        target_size=image_shape,
        batch_size=batch_size,
        class_mode='categorical',
        shuffle=False
    )

    class_indices = train_data.class_indices
    num_classes = train_data.num_classes

    with open(INDICES_DIR / "class_indices.json", "w") as json_file:
        json.dump(class_indices, json_file, indent=4)
    
    print("Class indices saved:", class_indices)

    return class_indices, train_data, test_data, valid_data, num_classes