import uuid
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    session
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
        #print('in endpoint /<invite_code>: current user is already authenticated')
        return redirect("/")

    # print('in endpoint /<invite_code>: code is ' + invite_code)

    # previous approach: compare in uuid format
    # strings are good enough for our purposes, and requires fewer formatting checks such as bad URLs
    #
    # foundFlag = False
    # for i in range(INVITE_LIMIT):
    #     if uuid.UUID(invite_code) == invite_codes[i]:
    #         foundFlag = True
    #         del invite_codes[i]
    #         break
    # if not foundFlag:
    #     flash("error in login_single_use_invite()", "error")

    if invite_code in invite_codes:
        invite_codes.remove(invite_code)
        user = User(id=invite_code)
        login_user(user)
        session["_username"] = "single-use guest"
        flash("successfully used single-use invite: " + invite_code, "success")
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