import unittest

from zcommons import ConfigDict


class ConfigDictTest(unittest.TestCase):

    def setUp(self) -> None:
        self.cd = ConfigDict({
            "a": {
                "b": {
                    "c1": 1,
                    "c2": 2,
                    "c": {
                        "d1": "v_d1",
                        "d2": "v_d2"
                    }
                }
            }
        })

    def test_exists(self):
        self.assertTrue("a.b.c.d1" in self.cd)
        self.assertFalse("a.b.d" in self.cd)
        self.assertTrue("a.b.c" in self.cd)

    def test_get(self):
        self.assertEqual(self.cd.get("a.b.c1"), 1)
        self.assertRaises(KeyError, lambda: self.cd["a.b.d"])
        self.assertIsNone(self.cd.get("a.b.d", None))

    def test_put(self):
        self.cd.setdefault("a.b.c1", 3)
        self.assertEqual(self.cd["a.b.c1"], 1)
        self.cd["a"]["b"]["c3"] = 3
        self.assertEqual(self.cd["a.b.c3"], 3)

    def test_keys(self):
        keys = list(self.cd.keys())
        self.assertEqual(keys[0], "a.b.c.d1")
        self.assertEqual(keys[1], "a.b.c.d2")
        self.assertEqual(keys[2], "a.b.c1")
        self.assertEqual(keys[3], "a.b.c2")

    def test_update(self):
        d = {
            "q.p": {
                "x": 11,
                "y": 12,
                "z": 13
            }
        }
        self.cd.update(d)
        self.assertEqual(self.cd["q.p.x"], 11)
        self.assertEqual(self.cd["q.p.z"], 13)

