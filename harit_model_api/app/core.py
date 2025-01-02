
# from strictyaml import YAML
from pathlib import Path
import sys
import os
file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

import yaml

def load_languages():

    """Load the languages list from the configuration file."""
    config_path = os.path.join(root, "app", "config.yml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config.get("languages", [])

if __name__ == "__main__":
    load_languages()