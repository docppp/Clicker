import datetime
import pyautogui

from timer import Timer

pyautogui.PAUSE = 0


class Event:

    def __init__(self):
        pass

    def process(self):
        pass

    @classmethod
    def createEvent(cls, event_type, *args):
        if issubclass(event_type, Event):
            return event_type(*args)
        return None


class MouseEvent(Event):

    def __init__(self, x: int, y: int):
        super().__init__()
        self._x = x
        self._y = y

    def process(self):
        now = datetime.datetime.now().time()
        print(f'[{now}] Mouse clicked at x={self._x} y={self._y}')
        pyautogui.click(self._x, self._y)

    def __str__(self):
        return f'mouse;x={self._x};y={self._y}'


class TimeEvent(Event):

    def __init__(self, timer_type, hour, minute, second, microsecond):
        super().__init__()
        self._type = timer_type
        self._h = hour
        self._m = minute
        self._s = second
        self._us = microsecond
        if timer_type == 'clock':
            self._timer = Timer.fromClock(hour, minute, second, microsecond)
        elif timer_type == 'duration':
            self._timer = Timer.fromDuration(hour, minute, second, microsecond)
        else:
            raise ValueError("Invalid timer type.")

    def process(self):
        t = 'until systime' if self._type == 'clock' else 'for'
        now = datetime.datetime.now().time()
        print(f'[{now}] Timer waits {t} {self._h:02d}:{self._m:02d}:{self._s:02d}.{self._us:06d}')
        self._timer.waitForTimeout()

    def __str__(self):
        return f'time;t={self._type};h={self._h};m={self._m};s={self._s};u={self._us}'
