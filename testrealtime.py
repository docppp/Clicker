import datetime
from timer import Timer


class Clock:

    def __init__(self, hour, minute, second, microsecond):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        self.precision = 100

    def set_precision(self, value):
        self.precision = value

    def step(self):
        self.microsecond += self.precision
        if self.microsecond > 99999:
            self.second += self.microsecond / 1000000
            self.microsecond %= 1000000
        if self.second > 59:
            self.minute += self.second / 60
            self.second %= 60
        if self.minute > 59:
            self.hour += self.minute / 60
            self.minute %= 60
        if self.hour > 23:
            self.hour %= 24

    def getCurrentTime(self):
        return [self.hour, self.minute, self.second, self.microsecond]


class MockTimer(Timer):

    def __init__(self, clock: Clock):
        super().__init__()
        self.clock = clock

    def _getDeltaTime(self):
        now = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, self.clock.hour,
                                self.clock.minute, self.clock.second, self.clock.microsecond)
        start = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, now.hour,
                                  now.minute, now.second, now.microsecond)
        stop = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, self._timeout.hour,
                                 self._timeout.minute, self._timeout.second, self._timeout.microsecond)
        delta = stop - start
        return delta


def test():
    pass


if __name__ == '__main__':
    test()
