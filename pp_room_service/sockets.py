from flask import request, render_template
from flask_socketio import join_room
from flask_httpauth import HTTPDigestAuth
import yaml

from app import app, socket
from pp_room_service.guest_list import is_authentic_guest, get_authed_guest
from pp_config.secrets import get_secret

USER_ID = "offkai_pp_uid"

auth = HTTPDigestAuth()
auth_users = yaml.safe_load(str(get_secret("admin_auth")))

user_manifest = {}
room_manifest = { "waiting": [], "room1": "", "room2": "", "room3": "" }

def is_admin_token(token):
    return token == "admin"

def is_user_token(token):
    return is_authentic_guest(token)

@auth.get_password
def verify_admin(username):
    return auth_users.get(username, None)

@socket.on("connect")
def user_connect(auth):
    if auth is None or "token" not in auth:
        return False
    elif is_user_token(auth["token"]):
        handle_user_connect(auth["token"])
    else:
        return False

def handle_user_connect(token):
    guest = get_authed_guest(token)
    if guest is None:
        join_room("unauthed... this should never happen")
    user = guest.name
    join_room(user)
    room_manifest["waiting"].append(user)
    socket.emit("assignName", { "name": user }, to=user)
    socket.emit("userConnected", { "user": user }, namespace="/admin", to="admin")

@socket.on('disconnect')
def user_disconnect():
    #  TODO handle user disconnect server-side logic
    print("disconnected")
    print(request.sid)
    # socket.emit("userDisconnected", { "user": data["user"] }, namespace="/admin")


#
# ADMIN SOCKETS
#
@socket.on("connect", namespace="/admin")
def admin_connect(auth):
    print("admin connected")
    if auth is None or "token" not in auth:
        print ("Reject, no token")
        return False
    elif is_admin_token(auth["token"]):
        print ("Accept admin")
        join_room("admin")
    else:
        print ("Reject, bad token")
        return False

@socket.on("addUserToken", namespace="/admin")
def add_user(data):
    user_manifest[data["token"]] = data["user"]

@socket.on("move", namespace="/admin")
def move_user(data):
    #  TODO handle user move server-side logic
    print("move requested")
    print(data)
    print(room_manifest)
    socket.emit("moveUser", data, to="admin")
    socket.emit("moveUser", (data["to"] != 0), to=data["user"])

@socket.on("pingRoom", namespace="/admin")
def ping_room(data):
    if data["room"] == 0:
        socket.emit("ping")
    else:
        room = "room" + str(data["room"])
        user = room_manifest[room]
        socket.emit("ping", to=user)


if __name__ == "__main__":
    socket.run(app, port=5000)