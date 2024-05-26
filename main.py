from app import app, socket, port
from pp_auth import invites
from pp_blueprints import admin_blueprint, guest_blueprint, landing_blueprint
from pp_config.configurations import load_config
from pp_config.args import parser

args = parser.parse_args()

load_config(str(args.config[0]))

app.register_blueprint(invites.bp)
app.register_blueprint(admin_blueprint.bp)
app.register_blueprint(guest_blueprint.bp)
app.register_blueprint(landing_blueprint.bp)
from pp_room_service import room_controller
socket.run(app, host="0.0.0.0", port=port)
