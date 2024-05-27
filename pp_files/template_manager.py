from pathlib import Path
from pp_config.configurations import get_config

templates = {}

def load_templates():
    path = get_config()["templateRoot"]
    for file in Path(path).iterdir():
        templates[file.name.split(".")[0]] = file.absolute

def get_template_names():
    return templates.keys()
