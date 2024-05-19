from flask import (
    Blueprint,
    render_template,
    redirect
)
from pathlib import Path
import os
import random
import string
from pp_files.guest import Guest

bp = Blueprint("templates_controller", __name__)

templates = []

# load_templates():
#
# expected csv formatting:
#
# 0: name                # OK to include whitespace, capitalization, and periods; replace accents / avoid commas
# 1: filename of front   # can be blank; one talent in 2024 should have no associated card images
# 2: filename of back    # same ^
# 3: day                 # encoded as {0, 1, 2, 3}, representing friday saturday sunday or no plotter usage, respectively
# 4: is group?           # encoded as 0 or 1, for solo session and group session, respectively
# 5: group code          # '' or a number 0 to 3; only applies to multiple talents sharing the same session
# 6: orientation         # encoded as {'h', 'v', ''} for whether the image is portrait landscape or n/a, respectively
#
# no header row
#
# all conversion of types is handled within the scope of the Guest class constructor
#
# there's little to no validity checking yet, so make sure outside of the program that the data source will give no errors

def load_templates():
    i = 0
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, "../pp_data/guest_data.csv")
    with open(data_path) as fp:
        for line in fp:
            cells = line.split(",")
            templates.append(Guest(i, cells[0], cells[1], cells[2], cells[3], cells[4], cells[5], cells[6]))
            i += 1

def get_templates_by_day(day_in):
    # this is a copy, so it doesn't mutate the templates variable at top scope
    filtered_result = []
    for t in templates:
        if int(t.day) == int(day_in) or day_in == 4:
            filtered_result.append(t)
    return filtered_result

def get_random_slug(length=4):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))


load_templates()

@bp.route("/admin/2.5/", defaults={"day_in": 4}, methods=["GET"])
@bp.route("/admin/2.5/<int:day_in>", methods=["GET"])
def render_admin_page(day_in):
    if day_in >= 0 and day_in <= 2:
        day_code = day_in
    else:
        day_code = 4
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
