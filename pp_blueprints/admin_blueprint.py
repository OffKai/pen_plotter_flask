import yaml

from flask import Blueprint, render_template
from flask_httpauth import HTTPDigestAuth

from pp_config.secrets import get_secret

bp = Blueprint('admin', __name__, url_prefix='/oke_pp_admin')

auth = HTTPDigestAuth()
auth_users = yaml.safe_load(str(get_secret("admin_auth")))

@auth.get_password
def get_admin(username):
    return auth_users.get(username, None)

@bp.route("/", methods=["GET"])
@auth.login_required
def admin_page():
    return render_template("test_admin.html")
