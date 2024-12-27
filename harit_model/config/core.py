import sys
from pathlib import Path

# Path setup
file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

from typing import Dict

from pydantic import BaseModel
from strictyaml import YAML, load
import harit_model
# Project Directories
PACKAGE_ROOT = Path(harit_model.__file__).resolve().parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "dataset"
TRAINED_MODEL_DIR = PACKAGE_ROOT / "trained_models"
INDICES_DIR = PACKAGE_ROOT / "indices"

class KaggleHubConfig(BaseModel):
    dataset: str
    output_dir: str
   
class ClearMLConfig(BaseModel):
    project: str
    dataset: str
    output_dir: str   
    

class AppConfig(BaseModel):
    package_name: str
    kagglehub: KaggleHubConfig
    clearmlconfig: ClearMLConfig
    data_dir: str
    test_data_dir: str
    pipeline_name: str
    pipeline_save_file: str

class ModelConfig(BaseModel):
    test_size: float
    random_state: int
    epochs: int
    batch_size: int

class Config(BaseModel):
    app_config: AppConfig
    model_config: ModelConfig

def find_config_file() -> Path:
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH!r}")

def fetch_config_from_yaml(cfg_path: Path = None) -> YAML:
    if not cfg_path:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as conf_file:
            return load(conf_file.read())
    raise OSError(f"Did not find config file at path: {cfg_path}")

def create_and_validate_config(parsed_config: YAML = None) -> Config:
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    # Separate app_config and model_config
    app_config_data = {
        "package_name": parsed_config.data["package_name"],
        "kagglehub": parsed_config.data["kagglehub"],
        "clearmlconfig" : parsed_config.data["clearml"]
        "data_dir": parsed_config.data["data_dir"],
        "test_data_dir": parsed_config.data["test_data_dir"],
        "pipeline_name": parsed_config.data["pipeline_name"],
        "pipeline_save_file": parsed_config.data["pipeline_save_file"],
    }
    
    model_config_data = {
        "test_size": parsed_config.data["test_size"],
        "random_state": parsed_config.data["random_state"],
        "epochs": parsed_config.data["epochs"],
        "batch_size": parsed_config.data["batch_size"],
    }

    return Config(
        app_config=AppConfig(**app_config_data),
        model_config=ModelConfig(**model_config_data),
    )

config = create_and_validate_config()