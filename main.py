from app import app, socket, port
from pp_blueprints import admin_blueprint, guest_blueprint, landing_blueprint
from pp_config.configurations import load_config
from pp_config.args import parser

args = parser.parse_args()

load_config(str(args.config[0]))

if args.dev:
    import test
else:
    app.register_blueprint(admin_blueprint.bp)
    app.register_blueprint(guest_blueprint.bp)
    app.register_blueprint(landing_blueprint.bp)
    from pp_room_service import sockets
    socket.run(app, host="0.0.0.0", port=port)
