import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import tensorflow as tf
import numpy as np
import os
import json


from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator

from harit_model.config.core import config
from harit_model.config.core import TRAINED_MODEL_DIR, INDICES_DIR

def preprocess_image(img_path, target_size=(224, 224)):
    img = load_img(img_path, target_size=(224, 224))  # Resize image
    img_array = img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
    img_array = preprocess_input(img_array)  # Normalize image
    return img_array

# Extract features using flow_from_directory
def train_test_valid(data_dir, target_size=(224, 224), batch_size=config.model_config.batch_size):
    # Data generator for loading and preprocessing images
    train_datagen = ImageDataGenerator(rescale=1/255., validation_split=config.model_config.test_size)
    test_datagen = ImageDataGenerator(rescale = 1/255.)


    # Generate batches of image data with labels
    # load training data
    print("Training Images:")
    image_shape = (224,224)
    batch_size = 64
    train_data = train_datagen.flow_from_directory(data_dir+'train/',
                                               target_size=image_shape,
                                               batch_size=batch_size,
                                               class_mode='categorical',
                                               shuffle=True,
                                               subset='training')

    # load validation data (20% of training data)
    print("Validating Images:")
    valid_data = train_datagen.flow_from_directory(data_dir+'train/',
                                                target_size=image_shape,
                                                batch_size=batch_size,
                                                class_mode='categorical',
                                                shuffle=False,
                                                subset='validation')

    # load test data (consider validation data as test data)
    print('Test Images:')
    test_data = test_datagen.flow_from_directory(data_dir+'valid/',
                                                target_size=image_shape,
                                                batch_size=batch_size,
                                                class_mode='categorical',
                                                shuffle=False)

    # Save class indices mapping (useful for decoding predictions later)
    class_indices = train_data.class_indices
    num_classes = train_data.num_classes

    #save the class indices for future prediction
    with open(INDICES_DIR/"class_indices.json", "w") as json_file:
            json.dump(class_indices, json_file)
    
    print("Class indices saved:", class_indices)

    return class_indices, train_data, test_data,valid_data,num_classes