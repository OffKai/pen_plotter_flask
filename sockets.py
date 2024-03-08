from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
app.secret_key = "secret!"
basic_auth = HTTPBasicAuth()
basic_auth_users = { "oke_admin": "admin" }

socket = SocketIO()
socket.init_app(app)

user_manifest = { "waiting_room": [], "room1": [], "room2": [], "room3": []}

@basic_auth.verify_password
def verify_admin(username, password):
    if username in basic_auth_users and password == basic_auth_users[username]:
        return username
    else:
        return None

@app.get("/")
def user():
    return render_template("test.html")

@app.get("/admin")
@basic_auth.login_required
def admin():
    return render_template("test_admin.html")

@socket.on("connect")
def connect(auth):
    print(auth)
    print("connect")

@socket.on("newUser")
def chat(data):
    print("user connected")
    print(data)
    join_room("room1")
    socket.emit("userConnected", data)

@socket.on("move")
def chat(data):
    print("move requested")
    print(data)
    socket.emit("moveUser", data, to="room1")
    socket.emit("moveUser", data, to="room2")
    socket.emit("moveUser", data, to="room3")

@socket.on("ackMove")
def chat(data):
    leave_room(data["from"])
    join_room(data["to"])

@socket.on("click")
def click():
    socket.emit("chat_message", "button clicked")

@socket.on("pingRoom")
def ping_room(data):
    room = "room" + str(data["room"])
    socket.emit("ping", to=room)

if __name__ == "__main__":
    socket.run(app, port=5000)