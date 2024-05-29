from flask import Blueprint, render_template, session, redirect

bp = Blueprint('guest', __name__, url_prefix='/pp')

@bp.route("/")
def index():
    return render_template("index.html")


# @bp.route("/en", methods=["GET", "POST"])
# def lang_en():
#     session["locale"] = "en"
#     return redirect("/")


# @bp.route("/jp", methods=["GET", "POST"])
# def lang_jp():
#     session["locale"] = "ja"
#     return redirect("/")
