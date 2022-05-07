import multiprocessing
import random
import unittest

import zcommons as zc
import tests


global_counter: zc.Counter = None


def run(counter, inc_num, dec_num):
    global global_counter
    if counter is None:
        counter = global_counter
    loop_num = inc_num + dec_num
    inc_cnt, dec_cnt = 0, 0
    for _ in range(loop_num):
        if inc_cnt == inc_num:
            counter.dec()
            dec_cnt += 1
            continue

        if dec_cnt == dec_num:
            counter.inc()
            inc_cnt += 1
            continue

        rv = random.randint(1, loop_num)
        if rv <= inc_num:
            counter.inc()
            inc_cnt += 1
        else:
            counter.dec()
            dec_cnt += 1


def multi_thread_inc(counter, thread_num, inc_num, dec_num):
    global global_counter
    global_counter = counter

    tg = zc.ThreadGroup()
    for _ in range(thread_num):
        tg.add(target=run, args=(None, inc_num, dec_num))
    tg.start()
    tg.join()


def multi_process_inc(counter, process_num, inc_num, dec_num):
    procs = []
    for _ in range(process_num):
        procs.append(multiprocessing.Process(target=run, args=(counter, inc_num, dec_num)))
    for p in procs:
        p.start()
    for p in procs:
        p.join()


class CounterTest(unittest.TestCase):

    def setUp(self) -> None:
        self.thread_num = 10
        self.inc_num = 200000
        self.dec_num = 100000
        self.cnt = zc.Counter(0, 1)
        self.lf_cnt = zc.LockFreeCounter(1, 2)
        self.mt_cnt = zc.MultiThreadCounter(2, 3)
        self.mp_cnt = zc.MultiProcessCounter(3, 4)

    def test_base(self):
        for _ in range(1000):
            self.cnt.inc()
            self.lf_cnt.inc()
            self.mt_cnt.inc()
            self.mp_cnt.inc()
        self.assertEqual(self.cnt.count(), 1000)
        self.assertEqual(self.lf_cnt.count(), 2001)
        self.assertEqual(self.mt_cnt.count(), 3002)
        self.assertEqual(self.mp_cnt.count(), 4003)
        for _ in range(100):
            self.cnt.dec()
            self.lf_cnt.dec()
            self.mt_cnt.dec()
            self.mp_cnt.dec()
        self.assertEqual(self.cnt.count(), 900)
        self.assertEqual(self.lf_cnt.count(), 1801)
        self.assertEqual(self.mt_cnt.count(), 2702)
        self.assertEqual(self.mp_cnt.count(), 3603)

    def test_multi_thread(self):
        multi_thread_inc(self.cnt, self.thread_num, self.inc_num, self.dec_num)
        self.assertNotEqual(self.cnt.count(), 0 + 1 * self.thread_num * (self.inc_num - self.dec_num))
        multi_thread_inc(self.lf_cnt, self.thread_num, self.inc_num, self.dec_num)
        self.assertEqual(self.lf_cnt.count(), 1 + 2 * self.thread_num * (self.inc_num - self.dec_num))
        multi_thread_inc(self.mt_cnt, self.thread_num, self.inc_num, self.dec_num)
        self.assertEqual(self.mt_cnt.count(), 2 + 3 * self.thread_num * (self.inc_num - self.dec_num))
        multi_thread_inc(self.mp_cnt, self.thread_num, self.inc_num, self.dec_num)
        self.assertEqual(self.mp_cnt.count(), 3 + 4 * self.thread_num * (self.inc_num - self.dec_num))

    def test_multi_process(self):
        multi_process_inc(self.cnt, self.thread_num, self.inc_num, self.dec_num)
        self.assertEqual(self.cnt.count(), 0)
        multi_process_inc(self.lf_cnt, self.thread_num, self.inc_num, self.dec_num)
        self.assertEqual(self.lf_cnt.count(), 1)
        # multi_process_inc(self.mt_cnt, self.thread_num, self.inc_num, self.dec_num)
        # self.assertEqual(self.mt_cnt.count(), 2)
        multi_process_inc(self.mp_cnt, self.thread_num, self.inc_num, self.dec_num)
        self.assertEqual(self.mp_cnt.count(), 3 + 4 * self.thread_num * (self.inc_num - self.dec_num))
