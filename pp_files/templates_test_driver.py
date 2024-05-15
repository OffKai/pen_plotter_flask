# based on template_manager.py from "admin_ui" branch

from pathlib import Path
from flask import (
    Blueprint,
    render_template,
    redirect
)

bp = Blueprint("templates_test_driver", __name__)

# dict structure:
# - top level key: full name of talent(s)    # time slots with multiple talents have the combined list of names, comma separated
# - top level values: another dict
# - - filename
# - - day                                    # 0, 1, or 2 for friday saturday sunday; for separating on UIs
templates = {}

def load_templates():
    for file in Path(Path(".").parent, "static/images/guest_templates").iterdir():
        templates[file.name.split(".")[1]] = {"filename": file.absolute, "day": file.name.split(".")[0]}

def get_template_names():
    return templates.keys()

def get_templates_by_day(day_in):
    # this is a copy, so it doesn't mutate the templates variable at top scope
    filtered_result = {}
    for key, value in templates.items():
        if int(value["day"]) == int(day_in) or int(value["day"]) == 3:
            filtered_result[key] = value
    return filtered_result


load_templates()

@bp.route("/admin/2.5/", defaults={"day_in": 3}, methods=["GET"])
@bp.route("/admin/2.5/<int:day_in>", methods=["GET"])
def render_admin_page(day_in):
    if day_in >= 0 and day_in <= 2:
        day_code = day_in
    else:        
        return render_template("test_invites_templates.html", guest_data = templates)
    return render_template("test_invites_templates.html", guest_data = get_templates_by_day(day_code))

@bp.route("/generate-invite/", defaults={"guest_in": ""}, methods=["GET"])
@bp.route("/generate-invite/<string:guest_in>", methods=["GET"])
def generate_invite(guest_in):
    return redirect("/admin/2.5/")
    if guest_in == "":
        return
    #for k in templates.keys: