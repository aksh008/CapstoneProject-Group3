
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

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.h5"
plant_disease_model = load_pipeline(file_name=pipeline_file_name)

def make_prediction(img_path):
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