import uuid
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    session,
    make_response,
    request
)
from flask_login import (
    login_user,
    logout_user,
    current_user
)
from config import *
from models import User

INVITE_LIMIT = 4
invite_codes = []
for i in range(INVITE_LIMIT):
    invite_codes.append(str(uuid.uuid4()))

user = Blueprint("user", __name__)


@user.route("/invite-codes", methods=["GET"])
def generate_invite():
    return render_template("generate.html", invite_codes = invite_codes)


@user.route("/login/invite/<invite_code>", methods=["GET"])
def login_single_use_invite(invite_code):
    if current_user.is_authenticated:
        print("in endpoint /<invite_code>: current user is already authenticated")
        return redirect("/")

    # print('in endpoint /<invite_code>: code is ' + invite_code)

    if invite_code in invite_codes:
        invite_codes.remove(invite_code)
        user = User(id=invite_code)
        login_user(user, remember=True)
        session["_username"] = invite_code
        flash("successfully used single-use invite: " + invite_code, "success")
        resp = make_response(render_template("redirect.html"))
        resp.set_cookie("authId", invite_code, max_age=604800, path="/")
        return resp
    else:
        flash("error in login_single_use_invite() for code: " + invite_code, "error")
        return redirect("/")


@user.route("/logout")
def logout():
    if current_user.is_authenticated:
        logout_user()
        if "_username" in session:
            session.pop("_username")

    return redirect("/")