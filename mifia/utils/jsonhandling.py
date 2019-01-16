import json
import typing


def jbytify(data: typing.Union[dict, list]) -> bytes:
    """Convert a dictionary or a list into a byte JSON string."""
    string = json.dumps(data)
    return bytes(string, encoding="utf8")


def dejbytify(data: bytes) -> typing.Union[dict, list]:
    string = str(data, encoding="utf8")
    return json.loads(string)
