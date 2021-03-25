import unittest, datetime
from timer import Timer


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
        d_hour = -3
        d_min = 2137
        d_sec = 99
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

    def checkWaitTime(self, h, m, s, u, ret):
        timer = Timer.fromDuration(h, m, s, u)
        self.assertEqual(ret, timer.getWaitTime())

    def test_getWaitTime(self):
        self.checkWaitTime(2, 20, 3, 300, 'm')
        self.checkWaitTime(0, 20, 3, 300, 'm')
        self.checkWaitTime(0, 2, 3, 300, 's')
        self.checkWaitTime(0, 0, 30, 300, 's')
        self.checkWaitTime(0, 0, 4, 300, 's')
        self.checkWaitTime(0, 0, 3, 300, 'u')
        self.checkWaitTime(0, 0, 0, 300, 'u')
        with self.assertRaises(ValueError):
            self.checkWaitTime(0, 0, 0, 0, 'u')
            self.checkWaitTime(0, 0, 0, -1, 'u')
            self.checkWaitTime(0, 0, -1, 0, 'u')
            self.checkWaitTime(0, -1, 0, 0, 'u')
            self.checkWaitTime(-1, 0, 0, 0, 'u')

    def test_IDC(self):
        self.assertTrue(Timer.IDC)


if __name__ == '__main__':
    unittest.main()
