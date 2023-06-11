import os
import uuid
from urllib.parse import quote_plus

from authlib.integrations.flask_client import OAuth
from flask import (
    Blueprint,
    flash,
    redirect,
    url_for,
    request,
    session,
)
from flask_babel import gettext
from flask_login import (
    login_required,
    login_user,
    logout_user,
    current_user,
)
from werkzeug.security import check_password_hash

from config import *
from models import User


DISCORD_API_BASE_URL = "https://discord.com/api/"
DISCORD_API_AUTHORIZE_URL = "https://discord.com/oauth2/authorize"
DISCORD_API_ACCESS_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_API_REVOKE_TOKEN_URL = "https://discord.com/api/oauth2/token/revoke"

DISCORD_CLIENT_ID = os.environ.get("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.environ.get("DISCORD_CLIENT_SECRET")
DISCORD_CLIENT_OAUTH2_SCOPES = "identify guilds.members.read"

STAFF_SERVER_ID = "864267081255616542"
STAFF_SERVER_STAFF_ROLE_ID = "864276628237713459"
GUEST_SERVER_ID = "1089761570713772153"
GUEST_SERVER_GUEST_ROLE_ID = "1089771478154743961"

BASIC_LOGIN_DIGEST = os.environ.get("BASIC_LOGIN_DIGEST")

oauth = OAuth()
oauth.register(
    name="discord",
    client_id=DISCORD_CLIENT_ID,
    client_secret=DISCORD_CLIENT_SECRET,
    authorize_url=DISCORD_API_AUTHORIZE_URL,
    authorize_params={"prompt": "consent"},
    access_token_url=DISCORD_API_ACCESS_TOKEN_URL,
    access_token_params=None,
    api_base_url=DISCORD_API_BASE_URL,
    client_kwargs={
        "scope": DISCORD_CLIENT_OAUTH2_SCOPES,
    },
)

user = Blueprint("user", __name__)


@user.route("/login/discord", methods=["POST"])
def login_discord():
    if current_user.is_authenticated:
        return redirect("/")

    redirect_url = url_for(".authorize_discord", _external=True)
    return oauth.discord.authorize_redirect(redirect_url)


@user.route("/login/basic", methods=["POST"])
def login_backup():
    if current_user.is_authenticated:
        return redirect("/")

    if session.get("locale") == "ja":
        msgs = [
            "ログインに成功しました！",
            "パスワードが正しくない。",
        ]
    else:
        msgs = ["Success!", "The password you entered was incorrect."]

    username = request.form["username"]
    password = request.form["password"]

    if check_password_hash(BASIC_LOGIN_DIGEST, password):
        user = User(id=uuid.uuid4())
        login_user(user)
        session["_username"] = username
        flash(msgs[0], "success")
    else:
        flash(msgs[1], "error")

    return redirect("/")


@user.route("/authorize/discord")
def authorize_discord():
    if current_user.is_authenticated:
        return redirect("/")

    if session.get("_flashes") is not None:
        session["_flashes"].clear()

    print(session.get("locale"))

    if session.get("locale") == "ja":
        msgs = [
            "ログインに成功しました！",  #
            "Discordアカウントには、ログインの権限がありません。",  #
            "ログインにエラーが発生しました。",
        ]
    else:
        msgs = [
            "Success!",
            "Your Discord account does not have permission to login.",
            "There was an error logging in.",
        ]

    try:
        oauth.discord.authorize_access_token()
        if is_staff() or is_guest():
            user = User(id=uuid.uuid4())
            login_user(user)
            user_info = oauth.discord.get(quote_plus("users/@me"))
            session["_username"] = user_info["username"]
            session["_discord_user"] = user_info.json()
            flash(msgs[0], "success")
        else:
            flash(msgs[1], "error")
    except:
        flash(msgs[2], "error")

    return redirect("/")


@user.route("/logout")
@login_required
def logout():
    logout_user()
    if "_username" in session:
        session.pop("_username")
    if "_discord_user" in session:
        session.pop("_discord_user")

    return redirect("/")


def is_staff():
    return has_server_role(STAFF_SERVER_ID, STAFF_SERVER_STAFF_ROLE_ID)


def is_guest():
    return has_server_role(GUEST_SERVER_ID, GUEST_SERVER_GUEST_ROLE_ID)


def has_server_role(server_id, role_id):
    resp = oauth.discord.get(quote_plus(f"users/@me/guilds/{server_id}/member"))
    if resp.ok:
        member = resp.json()
        for role in member["roles"]:
            if role == role_id:
                return True
    return False
