from glob import glob
from io import BytesIO
from zipfile import ZipFile
import os

from pp_config.configurations import get_config


guest_versions = dict()

def increment_guest_version(guest_name):
    guest_version = guest_versions.get(guest_name, None)
    if guest_version is None:
        guest_versions[guest_name] = 0
    else:
        guest_versions[guest_name] = guest_versions[guest_name] + 1
    return guest_versions[guest_name]

def svg_meta_to_file_name(guest_name, version=None):
    svg_version = guest_versions[guest_name] if version is None else version
    return get_config()["svgRoot"] + str(guest_name) + "_" + str(svg_version) + ".svg"

def svg_meta_to_file_name(guest_name, version=None):
    svg_version = guest_versions[guest_name] if version is None else version
    return get_config()["svgRoot"] + str(guest_name) + "_" + str(svg_version) + ".svg"

def save_svg_fs(guest_name, svg_content):
    increment_guest_version(guest_name)
    filename = svg_meta_to_file_name(guest_name)
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    svg = open(filename, "w")
    svg.write(str(svg_content))
    svg.close()

def load_svg_fs(guest_name, verision):
    svg = open(svg_meta_to_file_name(guest_name, version=verision), "r")
    svg_content = svg.read()
    svg.close()
    return svg_content

def load_all_svgs_as_zip_stream_fs(guest_name=""):
    zip_stream = BytesIO()
    with ZipFile(zip_stream, 'w') as zf:
        for file in glob(os.path.join(get_config()["svgRoot"], guest_name + "*.svg")):
            zf.write(file, os.path.basename(file))
    zip_stream.seek(0)
    return zip_stream

def save_svg_obj_store(guest_name, svg_content):
    raise RuntimeError("NOT IMPLEMENTED")

def load_svg_obj_store(guest_name):
    raise RuntimeError("NOT IMPLEMENTED")