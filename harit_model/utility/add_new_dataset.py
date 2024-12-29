import sys
import os
# Get the root directory of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Add the project root to sys.path
sys.path.append(project_root)

from clearml import Dataset
from harit_model.config.core import config, DATASET_DIR

def increment_version(version: str) -> str:
    """Increment the patch version (e.g., 1.0.0 -> 1.0.1)."""
    major, minor, patch = map(int, version.split("."))
    patch += 1  # Increment patch version
    return f"{major}.{minor}.{patch}"
           
if __name__ == "__main__":
    
    parent_datasets = Dataset.get(dataset_name=config.app_config.clearmlconfig.dataset, 
                                  dataset_project=config.app_config.clearmlconfig.project_name)
    print(parent_datasets.id)
    
    new_dataset_version = increment_version(parent_datasets.version)
    print("Parent dataset version: ", parent_datasets.version)
    print("New dataset version: ", new_dataset_version)

    dataset = Dataset.create(
        dataset_name=config.app_config.clearmlconfig.dataset,
        parent_datasets=[parent_datasets.id],
        dataset_version=new_dataset_version
    )
    # Add files to the dataset
    dataset.add_files(DATASET_DIR)

    # Upload the dataset to ClearML
    dataset.upload()  # Use upload to add the files to the ClearML server
    dataset.finalize()  # Finalize the dataset to make it immutable
    

