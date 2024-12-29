import sys
import os
# Get the root directory of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Add the project root to sys.path
sys.path.append(project_root)

from clearml import Dataset
from harit_model.config.core import config, DATASET_DIR

# Increment patch of the version string
def increment_version(version: str) -> str:
    """Increment the patch version (e.g., 1.0.0 -> 1.0.1)."""
    major, minor, patch = map(int, version.split("."))
    patch += 1  # Increment patch version
    return f"{major}.{minor}.{patch}"

# Delete dataset utility if required
def delete_dataset():
     dataset = Dataset.delete(
        dataset_id=None,
        dataset_name=config.app_config.clearmlconfig.dataset,
        dataset_project=config.app_config.clearmlconfig.project_name,
        force=True,
        entire_dataset = True
    )
     print("dataset deleted!!")

# Adds version 1.0.0 to ClearML
def add_dataset_first_time():
    dataset = Dataset.create(
        dataset_name=config.app_config.clearmlconfig.dataset,
        dataset_project=config.app_config.clearmlconfig.project_name,
        dataset_version="1.0.0" # as data is added first time version should be 1.0.0
    )
    dataset.add_files(DATASET_DIR)

    # Upload the dataset to ClearML
    dataset.upload()
    dataset.finalize()
    print("data uploaded!!")

# Adds new version of dataset in CLearML
def add_dataset_new_version():
    parent_datasets = Dataset.get(dataset_name=config.app_config.clearmlconfig.dataset, 
                                  dataset_project=config.app_config.clearmlconfig.project_name)
    print(parent_datasets.id)
    
    new_dataset_version = increment_version(parent_datasets.version)
    print("Parent dataset version: ", parent_datasets.version)
    print("New dataset version: ", new_dataset_version)

    dataset = Dataset.create(
        dataset_name=config.app_config.clearmlconfig.dataset,
        parent_datasets=[parent_datasets.id],
        dataset_project=config.app_config.clearmlconfig.project_name,
        dataset_version=new_dataset_version
    )
    
    # Add files to the dataset
    dataset.add_files(DATASET_DIR)

    # Upload the dataset to ClearML
    dataset.upload()
    dataset.finalize()
    print("data uploaded successfull !!")
    
if __name__ == "__main__":
    add_dataset_new_version()
    

