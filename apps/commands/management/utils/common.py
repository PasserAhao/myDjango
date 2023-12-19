import json


def value_format(value):
    try:
        result = json.loads(value)
    except json.JSONDecodeError:
        result = value
    return result
