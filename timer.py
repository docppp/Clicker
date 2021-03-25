import datetime
from time import sleep


class WAIT:
    """
    Class with constant variables, so no magic number is necessary
    """
    __slots__ = ()
    PRECISION_THRESHOLD = 3
    HOUR = 1
    MIN = 2
    SEC = 3
    USEC = 4


class Timer:
    """
    Timer class that sleeps until system time or until given duration passes
    """

    IDC = 1
    """"I Don't Care" variable - used when field does not matter"""

    def __init__(self):
        self._timeout = datetime.datetime.now().time()

    @classmethod
    def fromClock(cls, hour=0, minute=0, second=0, microsecond=0):
        """
        :param hour: [0, 23]
        :param minute: [0, 59]
        :param second: [0, 59]
        :param microsecond: [0, 99999]
        :return: Timer that waits until given system time
        """
        t = Timer()
        t._timeout = t._timeout.replace(hour, minute, second, microsecond)
        return t

    @classmethod
    def fromDuration(cls, hour=0, minute=0, second=0, microsecond=0):
        """
        :param hour: [0, 23]
        :param minute: [0, 59]
        :param second: [0, 59]
        :param microsecond: [0, 99999]
        :return: Timer that waits for given duration (must be greater that zero)
        """
        if hour < 0 or hour > 23:
            raise ValueError("Wrong hour value. Must be [0, 23]")
        if minute < 0 or minute > 59:
            raise ValueError("Wrong minute value. Must be [0, 59]")
        if second < 0 or second > 59:
            raise ValueError("Wrong second value. Must be [0, 59]")
        if microsecond < 0 or microsecond > 99999:
            raise ValueError("Wrong microsecond value. Must be [0, 99999]")
        if hour + minute + second + microsecond == 0:
            raise ValueError("Zero time value.")

        t = Timer()
        now = datetime.datetime.now()
        timeout = now + datetime.timedelta(hours=hour, minutes=minute, seconds=second, microseconds=microsecond)
        t._timeout = timeout.time()
        return t

    def waitForTimeout(self):
        try:
            while self.getWaitTime() == WAIT.MIN:
                sleep(60)
            while self.getWaitTime() == WAIT.SEC:
                sleep(1)
            while 1:
                if self._getDeltaTime() < datetime.timedelta():
                    return True
        except Exception:
            return False

    def getWaitTime(self):
        """
        Check for how much time Timer should sleep before next check

        :return: WAIT ENUM
        """
        delta = self._getDeltaTime()
        if delta < datetime.timedelta():
            delta += datetime.timedelta(days=1)
        return self._checkInterval(delta)

    def _getDeltaTime(self):
        now = datetime.datetime.now().time()
        start = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, now.hour,
                                  now.minute, now.second, now.microsecond)
        stop = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, self._timeout.hour,
                                 self._timeout.minute, self._timeout.second, self._timeout.microsecond)
        delta = stop - start
        return delta

    @staticmethod
    def _checkInterval(delta):
        h, m, s, u = map(int, str(delta).replace('.', ':').split(':'))
        if h > 0 or (h == 0 and m > WAIT.PRECISION_THRESHOLD):
            return WAIT.MIN
        if m > 0 or (m == 0 and s > WAIT.PRECISION_THRESHOLD):
            return WAIT.SEC
        return WAIT.USEC
