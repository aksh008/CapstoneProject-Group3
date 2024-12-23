from pathlib import Path
import sys

import numpy as np
import tensorflow as tf
from PIL import Image, ImageEnhance

file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

def is_image(image_path):
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except (IOError, SyntaxError):
        return False

def validate_enhance_image_quality(image):
    # Resize image if necessary
    if image.shape[0] < 224 or image.shape[1] < 224:
        image = tf.image.resize(image, (224, 224))

    # Enhance brightness if necessary
    brightness = tf.reduce_mean(image)
    if brightness < 50:
        image = tf.image.adjust_brightness(image, delta=0.2)

    # Enhance sharpness if necessary
    gray_image = tf.image.rgb_to_grayscale(image)
    sharpness = tf.math.reduce_variance(tf.image.sobel_edges(gray_image))
    if sharpness < 2:
        image = tf.image.adjust_sharpness(image, factor=2.0)

    return image

def evaluate_model(model, test_data):
    print("Evaluating the model...")
    val_loss, val_accuracy = model.evaluate(test_data)
    return val_loss, val_accuracy