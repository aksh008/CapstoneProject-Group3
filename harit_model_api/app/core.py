
import yaml
# from strictyaml import YAML

def load_languages(config_path="harit_model_api\\app\config.yml"):
    """Load the languages list from the configuration file."""
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
    return config.get("languages", [])
