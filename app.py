from functools import wraps
import mimetypes
import os
import secrets

from flask import Flask, request, session
from flask_login import LoginManager, current_user
from flask_socketio import SocketIO, disconnect
from werkzeug.middleware.proxy_fix import ProxyFix

from config import *
from pp_auth.models import User
from pp_files.templates_controller import bp

def authenticated_only(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
        else:
            return f(*args, **kwargs)

    return wrapped

def get_locale():
    if "locale" not in session:
        session["locale"] = request.accept_languages.best_match({"en", "ja"})

    return session["locale"]


# Windows registry can get this messed up, so overriding here
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")

port = int(os.environ.get("PORT", 5000))

# construct app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_host=1)
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)
app.register_blueprint(bp)

app.jinja_env.globals["get_locale"] = get_locale

#oauth.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

socket = SocketIO()
socket.init_app(app)

# import pp_room_service.old_sockets

@login_manager.user_loader
def load_user(id):
    return User(id)


if __name__ == "__main__":
    socket.run(app, host="0.0.0.0", port=port)
