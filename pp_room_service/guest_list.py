import random
import string
import uuid

from pp_auth.models import Guest

all_guests = dict()
authed_guests = dict()
invites = dict()

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

def print_guest_list():
    print("all:", all_guests)
    print("slugs:", invites)
    print("authed:", authed_guests)
