import time
import unittest

import zcommons as zc


class ThreadGroupTest(unittest.TestCase):

    def test_base(self):
        def run():
            time.sleep(0.1)

        tg = zc.ThreadGroup()
        tg.add(target=run)
        self.assertEqual(tg.alive_count(), 0)
        tg.start()
        self.assertFalse(tg.done())
        self.assertEqual(tg.alive_count(), 1)
        tg.join()
        self.assertTrue(tg.done())
        self.assertEqual(tg.alive_count(), 0)
        self.assertEqual(tg.count(), 1)

    def test_thread_count(self):
        def run(secs):
            time.sleep(secs)

        tg = zc.ThreadGroup()
        for i in range(10):
            tg.add(target=run, args=(0.2 + 0.2 * i, ))
        tg.start()
        time.sleep(0.1)
        for i in range(10):
            self.assertEqual(tg.alive_count(), 10 - i)
            time.sleep(0.2)
        tg.join()
        self.assertTrue(tg.done())
