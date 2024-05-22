from flask import (
    Blueprint,
    flash,
    make_response,
    redirect,
    render_template,
    session
)
from flask_httpauth import HTTPBasicAuth
from flask_login import (
    current_user,
    login_user,
    logout_user
)
import os
import random
import string
import uuid
from pp_files.guest import Guest
from pp_auth.models import User

templates_blueprint = Blueprint("templates_blueprint", __name__)

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

basic_auth = HTTPBasicAuth()
basic_auth_users = { "oke_admin": "iscutepassiton14" }

@basic_auth.verify_password
def verify_admin(username, password):
    if username in basic_auth_users and password == basic_auth_users[username]:
        return username
    else:
        return None

@templates_blueprint.route("/admin/2.5/", defaults={"day_in": 4}, methods=["GET"])
@templates_blueprint.route("/admin/2.5/<int:day_in>", methods=["GET"])
@basic_auth.login_required
def render_admin_page(day_in):
    if day_in >= 0 and day_in <= 2:
        day_code = day_in
    else:
        day_code = 4
    return render_template("admin_2.5.html", guest_data = get_templates_by_day(day_code))

@templates_blueprint.route("/generate-invite/", defaults={"guest_id_in": None}, methods=["GET"])
@templates_blueprint.route("/generate-invite/<int:guest_id_in>", methods=["GET"])
@basic_auth.login_required
def generate_invite(guest_id_in):
    current_day_tab = 4
    if guest_id_in == None:
        print("TODO: put flash() here")
    else:
        not_found_flag = True
        for t in templates:
            if t.id == guest_id_in:
                if t.invite_slug == "" or t.invite_slug == None:
                    t.invite_slug = get_random_slug()
                current_day_tab = t.day
                not_found_flag = False
                break
        if not_found_flag:
            print("TODO: put flash() here")
    return render_template("admin_2.5.html", guest_data = get_templates_by_day(current_day_tab))

@templates_blueprint.route("/test/gallery", methods=["GET"])
@basic_auth.login_required
def render_gallery_page():
    return render_template("gallery.html", guest_data = get_templates_by_day(4))

# should be eventually moved to a separate file, e.g. invites.py, but state is stored in this file (templates variable at top scope)
# can do some stuff to connect them, but taking the quick and dirty solution to reduce risk of things going wrong
@templates_blueprint.route("/login/<invite_code>", methods=["GET"])
def login_with_invite_link(invite_code):
    if current_user.is_authenticated or invite_code == None or invite_code == "":
        return redirect("/")

    not_found_flag = True
    for t in templates:
        if t.invite_slug == invite_code:
            my_uuid = str(uuid.uuid4())
            t.auth_id = my_uuid
            t.invite_slug = None
            my_user = User(id=t.id)
            login_user(my_user, remember=True)
            session["_username"] = t.name
            not_found_flag = False
            resp = make_response(render_template("redirect.html"))
            resp.set_cookie("auth_id", my_uuid, max_age=604800, path="/")
            resp.set_cookie("front_template_filename", t.front_image, max_age=604800, path="/")
            resp.set_cookie("back_template_filename", t.back_image, max_age=604800, path="/")
            resp.set_cookie("template_orientation", t.orientation, max_age=604800, path="/")
            return resp
    #if not_found_flag:

    flash("error in login_single_use_invite() for code: " + invite_code, "error")
    return redirect("/")

@templates_blueprint.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        if "_username" in session:
            session.pop("_username")
        if "_discord_user" in session:
            session.pop("_discord_user")

        resp = make_response(render_template("redirect.html"))
        resp.set_cookie("auth_id", "", max_age=604800, path="/")
        resp.set_cookie("front_template_filename", "", max_age=604800, path="/")
        resp.set_cookie("back_template_filename", "", max_age=604800, path="/")
        resp.set_cookie("template_orientation", "v", max_age=604800, path="/")
        return resp

    return redirect("/")