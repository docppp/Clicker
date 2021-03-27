from collections import Counter

from events import Event, MouseEvent, TimeEvent


class ScriptManager:

    def __init__(self):
        self.name = "script"
        self.eventList = []

    def addEvent(self, event_string):
        return validateEventString(event_string)


def validateEventString(event_string: str) -> bool:
    known_event_type = ["mouse", "time", "test"]

    event_type, *rest = event_string.split(';')
    rest = ";".join(rest)
    if event_type not in known_event_type:
        return False

    template = {}
    if event_type == "mouse":
        template = {'x': int, 'y': int}
    if event_type == "time":
        template = {'t': str, 'h': int, 'm': int, 's': int, 'u': int}
    if event_type == "test":
        template = {'x': str, 'y': int, 'z': str, 'ff': float}

    if not _validateArgs(rest, template):
        return False

    return True


def _validateArgs(string: str, template: dict) -> bool:
    try:
        args = string.split(';')
    except ValueError:
        return False

    keys = []
    values = []

    for arg in args:
        try:
            key, value = arg.split("=")
        except ValueError:
            return False
        keys.append(key)
        values.append(value)

    if Counter(keys) != Counter(template.keys()):
        return False

    for idx, value in enumerate(values):
        try:
            template[keys[idx]](value)
        except ValueError:
            return False
    return True

