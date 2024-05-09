from flask import Blueprint, render_template, session, redirect

bp = Blueprint('landing', __name__, url_prefix='/')

@bp.route("/")
def index():
    return render_template("landing.html")
