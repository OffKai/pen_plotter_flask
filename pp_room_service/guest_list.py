import random
import string
import uuid

from pp_auth.models import Guest

all_guests = dict()
authed_guests = dict()
invites = dict()
guest_rooms = dict()

#
# INVITE/AUTH LOGIC
#
def add_guest_to_guest_list(guest: Guest):
    all_guests[guest.name] = guest

def get_guest(guest_name: str):
    return all_guests.get(guest_name, None)

def get_guests_for_day(day: int):
    if day > 3:
        guests = all_guests.values()
    else:
        guests = filter(lambda guest: guest.day == day, all_guests.values())
    return sorted(guests, key=lambda guest: guest.name.lower())

def generate_slug_for_guest(guest_name: str):
    if guest_name not in all_guests:
        return None
    slug = get_new_slug()
    all_guests[guest_name].invite_slug = slug
    invites[slug] = guest_name
    return slug

def get_new_slug():
    slug = generate_random_slug(4)
    while slug in invites:
        slug = generate_random_slug(4)
    return slug

def generate_random_slug(length=4):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length))

def authenticate_slug(slug: str):
    if slug not in invites:
        return None
    guest_name = invites[slug]
    auth_id = str(uuid.uuid4())
    all_guests[guest_name].invite_slug = None
    all_guests[guest_name].auth_id = auth_id
    authed_guests[auth_id] = all_guests[guest_name]
    del invites[slug]
    return guest_name, auth_id

def is_authentic_guest(auth_id: str):
    return auth_id in authed_guests

def get_authed_guest(auth_id: str):
    return authed_guests.get(auth_id, None)

#
# ROOM LOGIC
#
def is_guest_in_room(guest_name):
    return guest_name in guest_rooms

def add_guest_to_waiting_room(auth_id: str):
    if is_authentic_guest(auth_id):
        guest = authed_guests[auth_id]
        guest_rooms[guest.name] = 0
        return 0

def move_guest_to_room(guest_name, room_index):
    if is_guest_in_room(guest_name):
        guest_rooms[guest_name] = room_index
        return room_index
    
def kick_guest(guest_name_or_auth_id):
    if guest_name_or_auth_id in all_guests:
        #it's guest_name
        guest = all_guests[guest_name_or_auth_id]
    elif guest_name_or_auth_id in authed_guests:
        #it's auth_id
        guest = authed_guests[guest_name_or_auth_id]
    guest_auth_id = guest.auth_id
    
    if guest_auth_id is None:
        return

    guest.auth_id = None
    del authed_guests[guest_auth_id]
    del guest_rooms[guest.name]

def get_room_manifest():
    return { "waiting": get_guests_in_room(0), "room1": get_guests_in_room(1), "room2": get_guests_in_room(2), "room3": get_guests_in_room(3) }

def get_guests_in_room(room_index):
    guests = list()
    for guest, room in guest_rooms.items():
        if room == room_index:
            guests.append(guest)
    return sorted(guests)

#
# DEBUG
#
# def print_guest_list():
#     print("all:", all_guests)
#     print("slugs:", invites)
#     print("authed:", authed_guests)
#     print("rooms:", get_room_manifest())
