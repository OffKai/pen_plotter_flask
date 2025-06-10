import os

def get_secret(key):
    value = os.getenv("SECRET_" + str(key).upper().replace('-', '_'))
    if value is None:
        with open("/mount/secrets/" + str(key).lower().replace('-', '_')) as secret_reader:
            value = secret_reader.read()
    return value
