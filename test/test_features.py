import unittest
import pandas as pd
import numpy as np
import sys
import os

import pytest
import numpy as np

from harit_model import __version__ as _version
from harit_model.config.core import config, TRAINED_MODEL_DIR, INDICES_DIR
from harit_model.processing.features import preprocess_image
from harit_model.processing.data_manager import load_pipeline
# Sample Test Data (Modify based on your use case)
@pytest.fixture

img_array = preprocess_image(img_path)
@pytest.fixture
def sample_features():
    # Mock a feature vector
    return np.random.rand(128)

# Test: Image Preprocessing
def test_preprocess_image(sample_image):
    processed_image = preprocess_image(sample_image)
    assert processed_image.shape == (224, 224, 3), "Preprocessed image should have the correct dimensions."
    assert processed_image.dtype == np.float32, "Preprocessed image should be normalized to float32."

# Test: Feature Extraction
def test_extract_features(sample_image):
    features = extract_features(sample_image)
    assert isinstance(features, np.ndarray), "Extracted features should be a numpy array."
    assert len(features) > 0, "Feature vector should not be empty."

# Test: Classification
def test_classify_plant(sample_features):
    prediction = classify_plant(sample_features)
    assert isinstance(prediction, str), "Classification result should be a string."
    assert prediction in ["Plant A", "Plant B", "Plant C"], "Prediction should match expected class labels."

# Test: End-to-End Pipeline
def test_pipeline(sample_image):
    processed_image = preprocess_image(sample_image)
    features = extract_features(processed_image)
    prediction = classify_plant(features)
    
    assert isinstance(prediction, str), "Pipeline output should be a string."
    assert prediction in ["Plant A", "Plant B", "Plant C"], "Pipeline prediction should be valid."

if __name__ == "__main__":
    unittest.main()