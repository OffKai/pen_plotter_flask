import os

def get_secret(key):
    value = os.getenv("SECRET_" + str(key).upper())
    if value is None:
        with open("/run/secrets/" + str(key).lower()) as secret_reader:
            value = secret_reader.read()
    return value
