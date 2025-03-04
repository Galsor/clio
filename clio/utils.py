import base64
import hashlib
import json


def generate_short_id(content, length=15):
    match type(content):
        case str():
            input_string = content
        case dict() | list():
            input_string = json.dumps(content)
        case _:
            input_string = repr(content)

    hash_obj = hashlib.sha256(input_string.encode()).digest()
    short_id = base64.urlsafe_b64encode(hash_obj).decode()[:length]
    return short_id


# Custom log format
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(funcName)s() | %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
