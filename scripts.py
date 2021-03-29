import datetime
from collections import Counter

from events import Event, MouseEvent, TimeEvent


class ScriptManager:

    templates = {'mouse': {'x': int, 'y': int},
                 'time': {'t': str, 'h': int, 'm': int, 's': int, 'u': int},
                 'test': {'x': str, 'y': int, 'z': str, 'ff': float}}

    def __init__(self):
        self.name = "unnamed_script"
        self.eventList = []

    def loadScript(self, script_path):
        self.eventList.clear()
        try:
            with open(script_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if not self.addEvent(line):
                        return False
            self.name = script_path
        except FileNotFoundError:
            return False

    def saveScript(self, script_path):
        try:
            with open(script_path, 'x') as file:
                file.writelines([f'{str(e)}\n' for e in self.eventList])
                return True
        except FileExistsError:
            return False

    def run(self, dommy=None):
        print(f'[{datetime.datetime.now().time()}] Script {self.name} start..')
        for e in self.eventList:
            e.process()
        print(f'[{datetime.datetime.now().time()}] Complete')
        return True

    def addEvent(self, event_string: str) -> bool:
        if self._validateEventString(event_string):
            self.eventList.append(self._createEvent(event_string))
            return True
        return False

    @staticmethod
    def _validateEventString(event_string: str) -> bool:
        event_type, *args = event_string.split(';')
        args = ";".join(args)
        if event_type not in ScriptManager.templates.keys():
            return False
        template = ScriptManager.templates.get(event_type)
        return ScriptManager._validateArgs(args, template)

    @staticmethod
    def _createEvent(event_string: str) -> Event:
        event_type, *args = event_string.split(';')
        param_dict = {}
        for arg in args:
            key, value = arg.split("=")
            param_dict[key] = value

        param_list = [ScriptManager.templates[event_type][p](param_dict[p])
                      for p in ScriptManager.templates[event_type]]

        e = Event.createEvent({'mouse': MouseEvent,
                               'time': TimeEvent}[event_type], *param_list)
        return e

    @staticmethod
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

