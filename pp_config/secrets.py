import os

def get_secret(key):
    return os.getenv("SECRET_" + str(key).upper())
