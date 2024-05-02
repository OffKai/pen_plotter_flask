from pp_config.configurations import get_config


def svg_meta_to_file_name(guest_name, attendee_name, version):
    return str(guest_name) + "." + str(attendee_name) + "." + str(version) + ".svg"

def save_svg_fs(guest_name, attendee_name, version, svg_content):
    svg = open(get_config()["svgRoot"] + svg_meta_to_file_name(guest_name, attendee_name, version), "w")
    svg.write(str(svg_content))
    svg.close()

def load_svg_fs(guest_name, attendee_name, version):
    svg = open(get_config()["svgRoot"] + svg_meta_to_file_name(guest_name, attendee_name, version), "r")
    svg_content = svg.read()
    svg.close()
    return svg_content

def save_svg_obj_store(guest_name, attendee_name, version, svg_content):
    print(guest_name, attendee_name, version, len(str(svg_content)))
    raise RuntimeError("NOT IMPLEMENTED")

def load_svg_obj_store(guest_name, attendee_name, version):
    print(guest_name, attendee_name, version)
    raise RuntimeError("NOT IMPLEMENTED")