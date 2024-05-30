from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    session
)
from flask_httpauth import HTTPDigestAuth
from flask_login import (
    current_user,
    login_user,
    logout_user
)
from math import floor
import os
import yaml

from pp_config.secrets import get_secret
from pp_auth.models import Guest
from pp_auth.models import User
from pp_room_service.guest_list import (
    add_guest_to_guest_list, 
    get_guest, 
    get_guests_for_day, 
    generate_slug_for_guest, 
    authenticate_slug
)

bp = Blueprint("templates_controller", __name__)

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
# - no header row
# - all conversion of types is handled within the scope of the Guest class constructor
# - there's little to no validity checking yet, so make sure outside of the program that the data source will give no errors

def load_templates():
    i = 0
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, "../pp_data/guest_data.csv")
    with open(data_path) as fp:
        for line in fp:
            cells = line.split(",")
            add_guest_to_guest_list(Guest(i, cells[0], cells[1], cells[2], cells[3], cells[4], cells[5], cells[6]))
            i += 1

load_templates()

auth = HTTPDigestAuth()
auth_users = yaml.safe_load(str(get_secret("admin_auth")))

@auth.get_password
def verify_admin(username):
    return auth_users.get(username, None)

@bp.route("/admin/2.5/", defaults={"day_in": 4}, methods=["GET"])
@bp.route("/admin/2.5/<int:day_in>", methods=["GET"])
@auth.login_required
def render_admin_page(day_in):
    day_code = floor(day_in) if day_in >= 0 and day_in < 3 else 4
    return render_template("admin_2.5.html", guest_data = get_guests_for_day(day_code))

@bp.route("/generate-invite/", defaults={"guest_name_in": None}, methods=["GET"])
@bp.route("/generate-invite/<guest_name_in>", methods=["GET"])
@auth.login_required
def generate_invite(guest_name_in):
    if guest_name_in == None:
        return None
    else:
        generate_slug_for_guest(guest_name_in)
    return redirect("/admin/2.5")

@bp.route("/test/gallery", methods=["GET"])
@auth.login_required
def render_gallery_page():
    return render_template("gallery.html", guest_data = get_guests_for_day(4))

@bp.route("/login/<invite_code>", methods=["GET"])
def login_with_invite_link(invite_code):
    if current_user.is_authenticated or invite_code == None or invite_code == "":
        return redirect("/")

    guest_name, auth_id = authenticate_slug(invite_code)
    if guest_name is None or auth_id is None:
        return redirect("/")
    
    guest = get_guest(guest_name)
    my_user = User(id=auth_id)
    session["_username"] = guest_name
    login_user(my_user, remember=True)

    resp = make_response(redirect("/"))
    resp.set_cookie("auth_id", auth_id, max_age=604800, path="/")
    resp.set_cookie("front_template_filename", guest.front_image, max_age=604800, path="/")
    resp.set_cookie("back_template_filename", guest.back_image, max_age=604800, path="/")
    resp.set_cookie("template_orientation", guest.orientation, max_age=604800, path="/")
    return resp

@bp.route("/logout")
def logout():
    if not current_user.is_authenticated:
        return redirect("/")

    logout_user()
    if "_username" in session:
        session.pop("_username")

    resp = make_response(redirect("/"))
    resp.set_cookie("auth_id", "", max_age=0, path="/")
    resp.set_cookie("front_template_filename", "", max_age=0, path="/")
    resp.set_cookie("back_template_filename", "", max_age=0, path="/")
    resp.set_cookie("template_orientation", "", max_age=0, path="/")
    return resp
