from flask import Blueprint, send_file
from flask_httpauth import HTTPDigestAuth
import yaml

from pp_config.secrets import get_secret
from pp_files.svg_manager import load_all_svgs_as_zip_stream_fs

auth = HTTPDigestAuth()
auth_users = yaml.safe_load(str(get_secret("admin_auth")))

bp = Blueprint('printer', __name__, url_prefix='/printer')

@bp.route("/svgs", defaults={"guest_name": None}, methods=["GET"])
@bp.route("/svgs/<guest_name>", methods=["GET"])
def get_svg(guest_name: str):
    if guest_name is None:
        zip_stream = load_all_svgs_as_zip_stream_fs()
        zip_name = "all_guests.zip"
    else:
        zip_stream = load_all_svgs_as_zip_stream_fs(guest_name)
        zip_name = guest_name + ".zip"
    return send_file(
        zip_stream,
        as_attachment=True,
        download_name=zip_name
    )
