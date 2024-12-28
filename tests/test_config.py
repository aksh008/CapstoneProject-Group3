import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from harit_model.config.core import AppConfig, ClearMLConfig, Config, ModelConfig
from harit_model.config.core import create_and_validate_config, fetch_config_from_yaml, find_config_file, CONFIG_FILE_PATH
import pytest
from pathlib import Path
from unittest.mock import patch, mock_open
from strictyaml import YAML
from pydantic import ValidationError

SAMPLE_YAML = """
    package_name: sample_package
    clearml:
        project_name: sample_project
        dataset: sample_dataset
        output_dir: /sample/output
        dataset_version: v1.0
        checkpoint_name: sample_checkpoint
        model_id: sample_model_id
    data_dir: /sample/data
    test_data_dir: /sample/test_data
    pipeline_name: sample_pipeline
    pipeline_save_file: sample_pipeline.pkl
    test_size: 0.2
    random_state: 42
    epochs: 10
    batch_size: 32
"""

def test_config_module():
    # Test find_config_file
    with patch('pathlib.Path.is_file', return_value=True):
        assert find_config_file() == CONFIG_FILE_PATH

    with patch('pathlib.Path.is_file', return_value=False):
        expected_error_message = re.escape(f"Config not found at {CONFIG_FILE_PATH!r}")
        with pytest.raises(Exception, match=expected_error_message):
            find_config_file()

    # Test fetch_config_from_yaml
    with patch('builtins.open', mock_open(read_data=SAMPLE_YAML)):
        yaml_config = fetch_config_from_yaml(Path('dummy_path'))
        assert isinstance(yaml_config, YAML)

    with patch('builtins.open', side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            fetch_config_from_yaml(Path('non_existent_path'))

    # Test create_and_validate_config
    with patch('builtins.open', mock_open(read_data=SAMPLE_YAML)):
        config = create_and_validate_config()

    # Validate Config object
    assert isinstance(config, Config)
    
    # Validate AppConfig
    assert isinstance(config.app_config, AppConfig)
    assert config.app_config.package_name == "sample_package"
    assert config.app_config.data_dir == "/sample/data"
    assert config.app_config.test_data_dir == "/sample/test_data"
    assert config.app_config.pipeline_name == "sample_pipeline"
    assert config.app_config.pipeline_save_file == "sample_pipeline.pkl"

    # Validate ClearMLConfig
    assert isinstance(config.app_config.clearmlconfig, ClearMLConfig)
    assert config.app_config.clearmlconfig.project_name == "sample_project"
    assert config.app_config.clearmlconfig.dataset == "sample_dataset"
    assert config.app_config.clearmlconfig.output_dir == "/sample/output"
    assert config.app_config.clearmlconfig.dataset_version == "v1.0"
    assert config.app_config.clearmlconfig.checkpoint_name == "sample_checkpoint"
    assert config.app_config.clearmlconfig.model_id == "sample_model_id"

    # Validate ModelConfig
    assert isinstance(config.model_config, ModelConfig)
    assert config.model_config.test_size == 0.2
    assert config.model_config.random_state == 42
    assert config.model_config.epochs == 10
    assert config.model_config.batch_size == 32

    print("All tests passed successfully!")
