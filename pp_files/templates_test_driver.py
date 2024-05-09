# based on template_manager.py from "admin_ui" branch

from pathlib import Path
from flask import (
    Blueprint,
    render_template,
)

bp = Blueprint("templates_test_driver", __name__)

templates = {}

def load_templates():
    for file in Path(Path(".").parent, "static/images/guest_templates").iterdir():
        templates[file.name.split(".")[0]] = file.absolute

def get_template_names():
    return templates.keys()

@bp.route("/invite-with-templates", methods=["GET"])
def generate_invite():
    load_templates()
    return render_template("test_invites_templates.html", guest_keys = get_template_names())