import yaml

from flask import Blueprint, make_response, render_template
from flask_httpauth import HTTPDigestAuth

from pp_config.secrets import get_secret
from pp_room_service.guest_list import get_room_manifest, get_guests_for_day

bp = Blueprint('admin', __name__, url_prefix='/admin')

auth = HTTPDigestAuth()
auth_users = yaml.safe_load(str(get_secret("admin_auth")))

@auth.get_password
def get_admin(username):
    return auth_users.get(username, None)

@bp.route("/", methods=["GET"])
@auth.login_required
def admin_page():
    auth_id = str(get_secret("admin_token"))
    resp = make_response(render_template("admin.html", guests = get_guests_for_day(4)))
    resp.set_cookie("auth_id", auth_id, max_age=604800, path="/")
    return resp

@bp.route("/user-manifest", methods=["GET"])
@auth.login_required
def user_manifest():
    return get_room_manifest()
