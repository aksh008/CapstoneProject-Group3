import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image,ImageEnhance
import tensorflow as tf

# Function to check if the file is an image
def is_image(image):
    try:
        img = Image.open(image)
        img.verify()  # Verify that it is, in fact, an image
        return True
    except (IOError, SyntaxError) as e:
        return False


# Image quality validation function
def validate_enhance_image_quality(image):
    
        # Get image resolution
    resolution = image.shape[:2]  # Height, Width
    if resolution[0]<224 or resolution[1]<224:
        # Resize the image
        image = image.resize((224,224))

    # Calculate brightness as mean pixel value
    brightness = np.mean(image)
    # Enhance brightness
    if brightness<50:
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
    

    # Calculate sharpness using Laplacian variance
    gray_image = tf.image.rgb_to_grayscale(image).numpy()
    sharpness = np.var(tf.image.sobel_edges(gray_image).numpy())
    if sharpness<2:
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(2.0)
    return image
    

def evaluate_model(model, test_data):
    print("Evaluating the model...")
    val_loss, val_accuracy = model.evaluate(test_data)
    return val_loss, val_accuracy
    # print(f"Validation Loss: {val_loss}")
    # print(f"Validation Accuracy: {val_accuracy}")

    # # Predictions and true labels
    # y_pred = np.argmax(model.predict(val_generator), axis=1)
    # y_true = val_generator.classes

    # # Classification Report
    # class_labels = list(val_generator.class_indices.keys())
    # print("Classification Report:")
    # print(classification_report(y_true, y_pred, target_names=class_labels))

    # # Confusion Matrix
    # cm = confusion_matrix(y_true, y_pred)
    # plot_confusion_matrix(cm, class_labels)

# def plot_confusion_matrix(cm, class_names):
#     """
#     Plot the confusion matrix.

#     Args:
#         cm (np.ndarray): Confusion matrix.
#         class_names (list): List of class names.
#     """
#     plt.figure(figsize=(10, 7))
#     sns.heatmap(cm, annot=True, fmt="d", xticklabels=class_names, yticklabels=class_names, cmap="Blues")
#     plt.xlabel("Predicted")
#     plt.ylabel("True")
#     plt.title("Confusion Matrix")
#     plt.show()
