import sys
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]
sys.path.append(str(root))

import kagglehub
import yaml
import os
import harit_model
PACKAGE_ROOT = Path(harit_model.__file__).resolve().parent

def download_dataset(config_path=PACKAGE_ROOT/"config.yml"):
    # Load the configuration
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)

    dataset = config['kagglehub']['dataset']
    output_dir = config['kagglehub']['output_dir']

    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Download the dataset
    print(dataset)
    path = kagglehub.dataset_download(dataset)
    print(f"Dataset downloaded to: {path}")
    return path


if __name__ == "__main__":
    download_dataset()