from timer import Timer
import pyautogui
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
        pyautogui.click(self._x, self._y)


class TimeEvent(Event):

    def __init__(self, timer_type, hour, minute, second, microsecond):
        super().__init__()
        if timer_type == 'clock':
            self._timer = Timer.fromClock(hour, minute, second, microsecond)
        elif timer_type == 'duration':
            self._timer = Timer.fromDuration(hour, minute, second, microsecond)
        else:
            raise ValueError("Invalid timer type.")

    def process(self):
        self._timer.waitForTimeout()
