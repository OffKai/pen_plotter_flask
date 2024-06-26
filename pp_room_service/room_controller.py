from flask import request, render_template, session
from flask_socketio import join_room
from flask_httpauth import HTTPDigestAuth
import logging
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
    logging.info("new user connection attempt")
    if auth is None or "token" not in auth:
        logging.info("connection fail: auth invalid", auth)
        return False
    elif is_user_token(auth["token"]):
        logging.info("connection success")
        handle_user_connect(auth["token"])
    else:
        logging.info("connection fail: auth failed")
        return False
    
@socket.on("connect", namespace="/plotter")
def plotter_connect():
    print("plotter connected")
    join_room("plotter")

def handle_user_connect(token):
    guest = get_authed_guest(token)
    logging.info(guest.name, "connected")
    if guest is None:
        logging.info("unauthed... this should never happen")
        return
    user = guest.name
    join_room(user)
    add_guest_to_waiting_room(token)
    socket.emit("assignName", { "name": user }, to=user)
    socket.emit("updateManifest", namespace="/admin", to="admin")

@socket.on("print")
def print_svg(data):
    save_svg_fs(get_authed_guest(data["guest"]), data["svg"])
    socket.emit("plot", {"svg": data["svg"]}, namespace="/plotter", to="plotter")


#
# ADMIN SOCKETS
#
@socket.on("connect", namespace="/admin")
def admin_connect(auth):
    logging.info("new admin connection attempt")
    if auth is None or "token" not in auth:
        logging.info("connection fail: auth invalid")
        return False
    elif is_admin_token(auth["token"]):
        logging.info("connection success")
        join_room("admin")
    else:
        logging.info("connection fail: auth failed")
        return False

@socket.on("move", namespace="/admin")
def move_user(data):
    logging.info("admin requested move:", data)
    move_guest_to_room(data["user"], data["to"])
    socket.emit("move", (data["to"] != 0), to=data["user"])
    socket.emit("updateManifest", get_room_manifest(), to="admin")

@socket.on("kick", namespace="/admin")
def kick_user(data):
    logging.info("admin requested kick:", data)
    kick_guest(data["user"])
    socket.emit("kick", to=data["user"])
    socket.emit("updateManifest", get_room_manifest(), to="admin")

@socket.on("ping", namespace="/admin")
def ping_room(data):
    logging.info("admin requested ping:", data)
    guests = get_guests_in_room(int(data["room"]))
    for guest in guests:
        socket.emit("ping", to=guest)


if __name__ == "__main__":
    socket.run(app, port=5000)
