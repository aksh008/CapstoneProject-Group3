
# from strictyaml import YAML
from pathlib import Path
import sys
import os
file = Path(__file__).resolve()
root = file.parents[1]
sys.path.append(str(root))

import yaml

# Initialize these as global variables
translations = {}
language_mapping = {}

def load_languages():

    """Load the languages list from the configuration file."""
    config_path = os.path.join(root, "app", "config.yml")
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config.get("languages", [])

def load_translations():
    """Load translations and language mapping from the translations file."""
    global translations, language_mapping
    translations_path = os.path.join(root, "app", "translations.yml")
    print(translations_path)
    with open(translations_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)

    translations = data.get('translations', {})
    language_mapping = data.get('language_mapping', {})
        # Print for debugging
    print("Available languages:", list(translations.keys()))
    print("Language mapping:", language_mapping)
    
load_translations()

if __name__ == "__main__":
    load_languages()
