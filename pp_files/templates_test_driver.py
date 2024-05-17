# based on template_manager.py from "admin_ui" branch

import random
import string
from pathlib import Path
from flask import (
    Blueprint,
    render_template,
    redirect
)
from pp_files.guest import Guest

bp = Blueprint("templates_test_driver", __name__)

templates = []

def load_templates():
    i = 0
    for file in Path(Path(".").parent, "static/images/guest_templates").iterdir():
        templates.append(Guest(file.name.split(".")[1], file.absolute, file.name.split(".")[0], i))
        i += 1

def get_templates_by_day(day_in):
    # this is a copy, so it doesn't mutate the templates variable at top scope
    filtered_result = []
    for t in templates:
        if int(t.day) == int(day_in) or day_in == 3:
            filtered_result.append(t)
    return filtered_result

def get_random_slug(length=4):
    return ''.join(random.choice(string.ascii_uppercase) for i in range(length))


load_templates()

@bp.route("/admin/2.5/", defaults={"day_in": 3}, methods=["GET"])
@bp.route("/admin/2.5/<int:day_in>", methods=["GET"])
def render_admin_page(day_in):
    if day_in >= 0 and day_in <= 2:
        day_code = day_in
    else:
        day_code = 3
    return render_template("test_invites_templates.html", guest_data = get_templates_by_day(day_code))

@bp.route("/generate-invite/", defaults={"guest_id_in": 255}, methods=["GET"])
@bp.route("/generate-invite/<int:guest_id_in>", methods=["GET"])
def generate_invite(guest_id_in):
    current_day_tab = 3
    not_found_flag = True
    for t in templates:
        if t.id == guest_id_in:
            if t.invite_slug == "":
                t.invite_slug = get_random_slug()
            not_found_flag = False
            current_day_tab = t.day
            break
    if not_found_flag:
        print("TODO: put flash() here")
    return render_template("test_invites_templates.html", guest_data = get_templates_by_day(current_day_tab))
