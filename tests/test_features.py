import pytest
import numpy as np
import json
from pathlib import Path
from unittest.mock import patch, mock_open

# Add the project root to sys.path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.processing.features import preprocess_image, train_test_valid

# Test for preprocess_image function
def test_preprocess_image():
    
    current_dir = Path(__file__).parent
    img_path = current_dir / "dummy.jpg"
    
    # Mock the load_img, img_to_array, and preprocess_input functions
    with patch('harit_model.processing.features.load_img') as mock_load_img, \
         patch('harit_model.processing.features.img_to_array') as mock_img_to_array, \
         patch('harit_model.processing.features.preprocess_input') as mock_preprocess_input:
        
        # Set up the mock returns
        mock_load_img.return_value = "dummy_img"
        mock_img_to_array.return_value = np.array([1, 2, 3])
        mock_preprocess_input.return_value = np.array([[1, 2, 3]])
        
        # Call the function
        result = preprocess_image(img_path)
        
        # Assert the result
        assert isinstance(result, np.ndarray)
        assert result.shape == (1, 3)  # Adjust based on your actual output shape
        
        # Check if the functions were called with correct arguments
        mock_load_img.assert_called_once_with(img_path, target_size=(224, 224))
        mock_img_to_array.assert_called_once()
        mock_preprocess_input.assert_called_once()

# Test for train_test_valid function
def test_train_test_valid():
    # Mock the ImageDataGenerator and its methods
    with patch('harit_model.processing.features.ImageDataGenerator') as mock_image_data_generator, \
         patch('builtins.open', mock_open()) as mock_file, \
         patch('json.dump') as mock_json_dump:
        
        # Set up the mock returns
        mock_flow = mock_image_data_generator.return_value.flow_from_directory
        mock_flow.return_value.class_indices = {"class1": 0, "class2": 1}
        mock_flow.return_value.num_classes = 2
        
        # Call the function
        data_dir = "dummy_data_dir/"
        class_indices, train_data, test_data, valid_data, num_classes = train_test_valid(data_dir)
        
        # Assert the results
        assert isinstance(class_indices, dict)
        assert len(class_indices) == 2
        assert num_classes == 2
        
        # Check if the methods were called with correct arguments
        assert mock_image_data_generator.call_count == 2  # Called for train and test
        assert mock_flow.call_count == 3  # Called for train, valid, and test
        
        # Check if json dump was called
        mock_json_dump.assert_called_once()
