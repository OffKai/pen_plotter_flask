from flask import request, render_template
from flask_socketio import join_room
from flask_httpauth import HTTPDigestAuth
import yaml

from app import app, socket
from pp_files.svg_manager import save_svg_fs
from pp_room_service.guest_list import is_authentic_guest, get_authed_guest
from pp_config.secrets import get_secret
from pp_room_service.guest_list import (
    add_guest_to_waiting_room,
    move_guest_to_room,
    kick_guest,
    get_guests_in_room,
    get_room_manifest
)

auth = HTTPDigestAuth()
auth_users = yaml.safe_load(str(get_secret("admin_auth")))

def is_admin_token(token):
    return token == get_secret("admin_token")

def is_user_token(token):
    return is_authentic_guest(token)

@auth.get_password
def verify_admin(username):
    return auth_users.get(username, None)

#
# USER SOCKETS
#
@socket.on("connect")
def user_connect(auth):
    print("A user connected")
    if auth is None or "token" not in auth:
        print("Illegal user auth", auth)
        return False
    elif is_user_token(auth["token"]):
        handle_user_connect(auth["token"])
    else:
        print("User failed to auth")
        return False

def handle_user_connect(token):
    guest = get_authed_guest(token)
    print("User connected: ", guest.name)
    if guest is None:
        join_room("unauthed... this should never happen")
    user = guest.name
    join_room(user)
    add_guest_to_waiting_room(token)
    socket.emit("assignName", { "name": user }, to=user)
    socket.emit("updateManifest", namespace="/admin", to="admin")

@socket.on("print")
def print_svg(data):
    save_svg_fs(get_authed_guest(data["guest"]), data["svg"])

#
# ADMIN SOCKETS
#
@socket.on("connect", namespace="/admin")
def admin_connect(auth):
    print("An admin connected")
    if auth is None or "token" not in auth:
        print("Illegal admin auth")
        return False
    elif is_admin_token(auth["token"]):
        print("Admin connected")
        join_room("admin")
    else:
        print("Admin failed to auth")
        return False

@socket.on("move", namespace="/admin")
def move_user(data):
    print("Admin requested to move user:", data)
    move_guest_to_room(data["user"], data["to"])
    socket.emit("move", (data["to"] != 0), to=data["user"])
    socket.emit("updateManifest", get_room_manifest(), to="admin")

@socket.on("kick", namespace="/admin")
def kick_user(data):
    print("Admin requested to kick user:", data)
    kick_guest(data["user"])
    socket.emit("kick", to=data["user"])
    socket.emit("updateManifest", get_room_manifest(), to="admin")
    print(get_room_manifest())

@socket.on("ping", namespace="/admin")
def ping_room(data):
    print("Admin requested to ping user:", data)
    guests = get_guests_in_room(int(data["room"]))
    for guest in guests:
        socket.emit("ping", to=guest)


if __name__ == "__main__":
    socket.run(app, port=5000)