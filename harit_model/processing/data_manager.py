from pathlib import Path
import sys
import os
file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

from pathlib import Path
import typing as t
import joblib
import shutil

from harit_model.processing.download_data import download_dataset
from harit_model.config.core import TRAINED_MODEL_DIR, config
from harit_model import __version__ as _version

def save_pipeline(pipeline_to_persist) -> None:
    """Persist the pipeline."""
    save_file_name = f"{config.app_config.pipeline_save_file}{_version}.h5"
    save_path = TRAINED_MODEL_DIR / save_file_name

    remove_old_pipelines(files_to_keep=[save_file_name])
    joblib.dump(pipeline_to_persist, save_path)
    
def remove_old_pipelines(*, files_to_keep: t.List[str]) -> None:
    """Remove old model pipelines."""
    do_not_delete = files_to_keep + ["__init__.py"]
    if(os.path.exists(TRAINED_MODEL_DIR)):
        for model_file in TRAINED_MODEL_DIR.iterdir():
            if model_file.name not in do_not_delete:
                model_file.unlink()

def copy_folder(source_folder, destination_folder):
    """Copy all files and subdirectories from source to destination."""
    if not os.path.exists(source_folder):
        raise FileNotFoundError(f"Source folder does not exist: {source_folder}")
    
    os.makedirs(destination_folder, exist_ok=True)

    for item in os.listdir(source_folder):
        source_item = os.path.join(source_folder, item)
        destination_item = os.path.join(destination_folder, item)

        if os.path.isdir(source_item):
            shutil.copytree(source_item, destination_item, dirs_exist_ok=True)
        else:
            shutil.copy2(source_item, destination_item)

    print(f"All files and subdirectories have been copied from {source_folder} to {destination_folder}.")

def load_dataset():
    print ("Getting the data from ClearMl Dataset")
    DATASET_DIR = download_dataset()
    print(f"Dataset downloaded and copied to {DATASET_DIR}")

def load_pipeline(*, file_name: str):
    """Load a persisted pipeline."""
    file_path = TRAINED_MODEL_DIR / file_name
    return joblib.load(filename=file_path)