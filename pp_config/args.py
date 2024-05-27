from argparse import ArgumentParser

parser = ArgumentParser(prog='Pen Plotter Application', description='Serves Pen Plotter guest UI, admin UI, and SVG store', epilog='Take care of the PPs!')
parser.add_argument("--config", nargs=1, required=True)
parser.add_argument("-d", "--dev", action="store_true")