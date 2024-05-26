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

def save_svg_fs(guest_name, svg_content):
    increment_guest_version(guest_name)
    svg = open(svg_meta_to_file_name(guest_name), "w")
    svg.write(str(svg_content))
    svg.close()

def load_svg_fs(guest_name, verision):
    svg = open(svg_meta_to_file_name(guest_name, version=verision), "r")
    svg_content = svg.read()
    svg.close()
    return svg_content

def save_svg_obj_store(guest_name, svg_content):
    print(guest_name, len(str(svg_content)))
    raise RuntimeError("NOT IMPLEMENTED")

def load_svg_obj_store(guest_name):
    print(guest_name)
    raise RuntimeError("NOT IMPLEMENTED")