import datetime


class Timer:
    IDC = 1
    """"I Don't Care" variable - used when field does not matter"""

    def __init__(self):
        self._timeout = datetime.datetime.now().time()

    @classmethod
    def fromClock(cls, hour, minute, second, microsecond):
        t = Timer()
        t._timeout = t._timeout.replace(hour, minute, second, microsecond)
        return t

    @classmethod
    def fromDuration(cls, hour=0, minute=0, second=0, microsecond=0):
        t = Timer()
        now = datetime.datetime.now()
        timeout = now + datetime.timedelta(hours=hour, minutes=minute, seconds=second, microseconds=microsecond)
        t._timeout = timeout.time()
        return t

