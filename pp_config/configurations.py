import yaml
from pathlib import Path

config = {}

def load_config(path):
    global config
    config = yaml.safe_load(Path(path).read_text())

def get_config():
    return config.copy()
