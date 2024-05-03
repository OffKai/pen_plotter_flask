from flask import Blueprint, render_template
from flask_httpauth import HTTPBasicAuth

bp = Blueprint('admin', __name__, url_prefix='/oke_pp_admin')

basic_auth = HTTPBasicAuth()
basic_auth_users = { "oke_admin": "admin" }

@basic_auth.verify_password
def verify_admin(username, password):
    if username in basic_auth_users and password == basic_auth_users[username]:
        return username
    else:
        return None

@bp.route("/", methods=["GET"])
@basic_auth.login_required
def admin_page():
    return render_template("test_admin.html")
