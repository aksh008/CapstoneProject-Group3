"""
Note: These tests will fail if you have not first trained the model.
"""
import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import numpy as np
import json
from harit_model import __version__ as _version
from harit_model.config.core import config, TRAINED_MODEL_DIR, INDICES_DIR
from harit_model.processing.features import preprocess_image
from harit_model.processing.data_manager import load_pipeline

def test_make_prediction(img_path):
    # Given
    try:
        with open(INDICES_DIR / "class_indices.json", "r") as json_file:
            class_indices = json.load(json_file)
    except FileNotFoundError:
        print("Class indices file not found")
        return None

    img_array = preprocess_image(img_path)
    predictions = plant_disease_model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)
    predicted_label = list(class_indices.keys())[predicted_class[0]]
    return predicted_label
