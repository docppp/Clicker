import datetime
from timer import Timer


class Clock:

    def __init__(self, hour, minute, second, microsecond):
        self.hour = hour
        self.minute = minute
        self.second = second
        self.microsecond = microsecond
        self.precision = 1000 * 10

    def set_precision(self, value):
        self.precision = value

    def step(self):
        self.microsecond += self.precision
        if self.microsecond > 99999:
            self.second += int(self.microsecond / 1000000)
            self.microsecond %= 1000000
        if self.second > 59:
            self.minute += int(self.second / 60)
            self.second %= 60
        if self.minute > 59:
            self.hour += int(self.minute / 60)
            self.minute %= 60
        if self.hour > 23:
            self.hour %= 24

    def getCurrentTime(self):
        return [self.hour, self.minute, self.second, self.microsecond]


class MockTimer(Timer):

    def __init__(self):
        super().__init__()
        self.clock = None
        self.wait_times = {'m': 0, 's': 0}

    def useClock(self, clock):
        self.clock = clock

    @classmethod
    def fromClock(cls, hour=0, minute=0, second=0, microsecond=0):
        t = Timer.fromClock(hour, minute, second, microsecond)
        mockt = MockTimer()
        mockt._timeout = t._timeout
        return mockt

    def _getDeltaTime(self):
        self.clock.step()
        now = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, self.clock.hour,
                                self.clock.minute, self.clock.second, self.clock.microsecond)
        start = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, now.hour,
                                  now.minute, now.second, now.microsecond)
        stop = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, self._timeout.hour,
                                 self._timeout.minute, self._timeout.second, self._timeout.microsecond)
        delta = stop - start
        return delta

    def _timerSleep(self, time):
        if time == 60:
            self.wait_times['m'] += 1
        else:
            self.wait_times['s'] += 1

        clock_steps = int(time * 1000000 / self.clock.precision)
        for _ in range(clock_steps - 1):
            self.clock.step()


def getDelta(future, now):
    d1 = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, future.hour,
                           future.minute, future.second, future.microsecond)
    d2 = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, now.hour,
                           now.minute, now.second, now.microsecond)
    return d1 - d2


def test():
    print("Mock test (1h, 31min, 10sec, 50000us)...")
    clock = Clock(12, 0, 0, 0)
    mock_timer = MockTimer.fromClock(13, 31, 10, 50000)
    mock_timer.useClock(clock)
    mock_timer.waitForTimeout()
    print("Minute waits:", mock_timer.wait_times['m'], ", Second waits:", mock_timer.wait_times['s'])
    print("Internal clock: ", mock_timer.clock.getCurrentTime())
    print()
    print("Real test (5s, 4000us)...")
    now = datetime.datetime.now().time()
    print("Current time:", now)
    real_timer = Timer.fromDuration(0, 0, 5, 4000)
    if real_timer.waitForTimeout():
        future = datetime.datetime.now().time()
        print("      Hit at:", future)
        print("        Took: ", getDelta(future, now))
    else:
        print("Interrupted, no hit.")


if __name__ == '__main__':
    test()
