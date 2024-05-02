import yaml
from pathlib import Path

config = {}

def load_config():
    global config
    config = yaml.safe_load(Path("config.yaml").read_text())

def get_config():
    return config.copy()
