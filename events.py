from timer import Timer
import pyautogui
pyautogui.PAUSE = 0


class Event:

    def __init__(self):
        pass

    def process(self):
        pass


class MouseEvent(Event):

    def __init__(self, x: int, y: int):
        super().__init__()
        self.x = x
        self.y = y

    def process(self):
        pyautogui.click(self.x, self.y)


class TimeEvent(Event):

    def __init__(self, timer: Timer):
        super().__init__()
        self.timer = timer

    def process(self):
        self.timer.waitForTimeout()
