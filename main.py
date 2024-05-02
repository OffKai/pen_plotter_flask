from app import app, socket, port
from pp_config.configurations import load_config, get_config
from pp_config.args import parser

args = parser.parse_args()

load_config(str(args.config[0]))

if args.dev:
    import test
else:
    socket.run(app, host="0.0.0.0", port=port)
