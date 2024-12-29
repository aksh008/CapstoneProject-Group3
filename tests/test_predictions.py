import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pytest
from harit_model.predict import make_prediction

def test_make_prediction():
    current_dir = Path(__file__).parent

    test_image_path = current_dir / "dummy.jpg"
    print(test_image_path)
    
    # Call the actual make_prediction function
    result = make_prediction(test_image_path)
    
    # Assertions
    assert result is not None, "Prediction should not be None"
    assert isinstance(result, str), "Prediction should be a string"
    
    print(f"Prediction result: {result}")
    