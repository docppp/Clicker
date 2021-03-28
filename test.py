import datetime
import unittest

from timer import Timer
from events import Event, MouseEvent, TimeEvent
from scripts import ScriptManager


class TestTimer(unittest.TestCase):

    def test_checkIfAllMethodsAreCovered(self):
        test_members = list(TestTimer.__dict__.keys())
        class_members = list(Timer.__dict__.keys())
        check_for = ['test_' + x for x in class_members if not x.startswith('_')]
        are_covered = all(test in test_members for test in check_for)
        if not are_covered:
            diff = list(set(check_for) - set(test_members))
            print("Timer functions that are not covered: ", diff)
            self.assertTrue(False)

    def test_fromClock(self):
        timer = Timer.fromClock(12, 0, 1, 123456)
        timeout = datetime.datetime(Timer.IDC, Timer.IDC, Timer.IDC, 12, 0, 1, 123456).time()
        self.assertTrue(timer._timeout, timeout)
        with self.assertRaises(ValueError):
            Timer.fromClock(0, 0, 0, 1000000)
            Timer.fromClock(0, 0, 60, 0)
            Timer.fromClock(0, 60, 0, 0)
            Timer.fromClock(24, 0, 0, 0)

    def test_fromDuration(self):
        d_hour = 21
        d_min = 37
        d_sec = 59
        d_usec = 100
        timer = Timer.fromDuration(d_hour, d_min, d_sec, d_usec)
        now = datetime.datetime.now()
        future = datetime.timedelta(hours=d_hour, minutes=d_min, seconds=d_sec, microseconds=d_usec)
        timeout = (now + future).time()
        h, m, s, u = timer._timeout.strftime('%H %M %S %f').split(' ')
        h2, m2, s2, u2 = timeout.strftime('%H %M %S %f').split(' ')
        self.assertEqual(h, h2)
        self.assertEqual(m, m2)
        self.assertEqual(s, s2)
        self.assertEqual(u, u2)  # This is kind of danger due to time needed to perform the test

    def getWaitTime(self, h, m, s, u, ret):
        timer = Timer.fromDuration(h, m, s, u)
        self.assertEqual(ret, timer.getWaitTime())

    def test_getWaitTime(self):
        from timer import WAIT
        self.getWaitTime(2, 20, 3, 300, WAIT.MIN)
        self.getWaitTime(0, 20, 3, 300, WAIT.MIN)
        self.getWaitTime(0, 2, 3, 300, WAIT.MIN)
        self.getWaitTime(0, 0, 30, 300, WAIT.SEC)
        self.getWaitTime(0, 0, 4, 300, WAIT.SEC)
        self.getWaitTime(0, 0, 3, 300, WAIT.SEC)
        self.getWaitTime(0, 0, 0, 300, WAIT.USEC)
        with self.assertRaises(ValueError):
            self.getWaitTime(0, 0, 0, 0, WAIT.USEC)
            self.getWaitTime(0, 0, 0, -1, WAIT.USEC)
            self.getWaitTime(0, 0, -1, 0, WAIT.USEC)
            self.getWaitTime(0, -1, 0, 0, WAIT.USEC)
            self.getWaitTime(-1, 0, 0, 0, WAIT.USEC)

    def test_waitForTimeout(self):
        """Passed here due to time dilatation. Tested in testrealtime.py"""
        pass

    def test_IDC(self):
        self.assertTrue(Timer.IDC)


class TestEvent(unittest.TestCase):

    def test_createEvent(self):
        e = Event.createEvent(MouseEvent, 1, 2)
        self.assertTrue(isinstance(e, MouseEvent))
        self.assertEqual(e._x, 1)
        self.assertEqual(e._y, 2)
        self.assertIsNone(Event.createEvent(Timer))


class TestScriptManager(unittest.TestCase):

    def test_validateEventString(self):
        s = ScriptManager()
        # as in temple
        self.assertTrue(s._validateEventString("test;x=str;y=10;z=abc;ff=10.0"))
        # other order
        self.assertTrue(s._validateEventString("test;ff=10.0;x=str;z=abc;y=10"))
        # int can be str
        self.assertTrue(s._validateEventString("test;ff=0;x=0;z=0;y=0"))
        # wrong type
        self.assertFalse(s._validateEventString("test;x=str;y=10;z=abc;ff=str"))
        # missing arg
        self.assertFalse(s._validateEventString("test;ff=10.0;x=str;z=abc"))
        # doubled arg
        self.assertFalse(s._validateEventString("test;ff=0;x=0;z=0;y=0;ff=0"))
        # corrupted
        self.assertFalse(s._validateEventString("test;ff===0;;=;0;=;;y=0;f;f=0"))

    def test_createEvent(self):
        e = ScriptManager._createEvent("mouse;y=100;x=50")
        self.assertEqual(e._x, 50)
        self.assertEqual(e._y, 100)


if __name__ == '__main__':
    unittest.main()
