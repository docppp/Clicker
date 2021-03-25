import datetime


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
        :param hour: [0,23]
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
        :return: Timer that waits for given duration (must be greater that zero)
        """
        t = Timer()
        now = datetime.datetime.now()
        timeout = now + datetime.timedelta(hours=hour, minutes=minute, seconds=second, microseconds=microsecond)
        t._timeout = timeout.time()
        return t

    def getWaitTime(self):
        """
        Check for how much time Timer should sleep before next check

        :return: 'm' | 's' | 'u'
        """
        delta = self._getDeltaTime()
        if delta < datetime.timedelta():
            raise ValueError("Timer error, event should happened in the past")
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
        if h > 0 or (h == 0 and m > 3):
            return 'm'
        if m > 0 or (m == 0 and s > 3):
            return 's'
        return 'u'



