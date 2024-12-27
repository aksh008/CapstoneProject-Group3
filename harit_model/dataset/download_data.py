from pathlib import Path
from harit_model import config
import kagglehub
import os


def download_dataset():
    kagglehub_config = config.app_config.kagglehub
    dataset = kagglehub_config.dataset
    output_dir = Path(kagglehub_config.output_dir)

    # Ensure output directory exists
    os.makedirs(output_dir,  exist_ok=True)

    # Download the dataset
    print(f"Downloading dataset: {dataset}")
    path = kagglehub.dataset_download(dataset)
    print(f"Dataset downloaded to: {path}")
    return path

if __name__ == "__main__":
    download_dataset()