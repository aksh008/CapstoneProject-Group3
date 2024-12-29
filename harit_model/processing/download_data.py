from pathlib import Path
import sys
import os
file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

# Add the project root to sys.path
sys.path.append(project_root)

from harit_model import config
from clearml import Dataset

def download_from_clearml(project_name, dataset, output_dir):
    dataset = Dataset.get(
        dataset_project=project_name,
        dataset_name=dataset,
        alias=f"{dataset}_latest",
        only_completed=True, 
        only_published=False,
    )

    local_path = dataset.get_mutable_local_copy(
        target_folder=output_dir,
        overwrite=True,
    )
    print("Dataset successfully downloaded to:", local_path)
    return local_path

def download_dataset():
    print("Going to download from ClearML")
    clearml_config = config.app_config.clearmlconfig
    project_name = clearml_config.project_name
    dataset = clearml_config.dataset
    output_dir = Path(clearml_config.output_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading dataset from ClearML: {dataset} from project: {project_name}")
    return download_from_clearml(project_name, dataset, output_dir)

if __name__ == "__main__":
    download_dataset()