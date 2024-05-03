from flask import request, render_template
from flask_socketio import join_room
from flask_httpauth import HTTPBasicAuth

from app import app, socket

USER_ID = "offkai_pp_uid"

basic_auth = HTTPBasicAuth()
basic_auth_users = { "oke_admin": "admin" }

user_manifest = {}
room_manifest = { "waiting": [], "room1": "", "room2": "", "room3": "" }

def is_admin_token(token):
    return token == "admin"

def is_user_token(token):
    return token in user_manifest

@basic_auth.verify_password
def verify_admin(username, password):
    if username in basic_auth_users and password == basic_auth_users[username]:
        return username
    else:
        return None

@socket.on("connect")
def user_connect(auth):
    print("User connected")
    print(auth)
    if auth is None or "token" not in auth:
        print ("Reject, no token")
        return False
    elif is_user_token(auth["token"]):
        print ("Accept user")
        handle_user_connect(auth["token"])
    else:
        print ("Reject, bad token")
        return False

def handle_user_connect(token):
    #  TODO handle user connect server-side logic
    user = user_manifest[token]
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
    socket.emit("moveUser", data, to=data["user"])

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