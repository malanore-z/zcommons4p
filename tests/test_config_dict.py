import unittest

from zcommons import ConfigDict


class ConfigDictTest(unittest.TestCase):

    def setUp(self) -> None:
        self.d = ConfigDict({
            "a": {
                "b": {
                    "c": {
                        "d1": "v_d1",
                        "d2": "v_d2"
                    },
                    "c1": 1,
                    "c2": 2
                }
            }
        })

    def test_exists(self):
        self.assertTrue("a.b.c.d1" in self.d)
        self.assertFalse("a.b.c" in self.d)
        self.assertTrue(self.d.exists("a.b.c", include_dict=True))

    def test_get(self):
        self.assertEqual(self.d.get("a.b.c1"), 1)
        self.assertRaises(KeyError, lambda: self.d["a.b.d"])
        self.assertIsNone(self.d.get("a.b.d"))

    def test_put(self):
        self.d.put_if_absent("a.b.c1", 3)
        self.assertEqual(self.d["a.b.c1"], 1)
        self.d["a"]["b"]["c3"] = 3
        self.assertEqual(self.d["a.b.c3"], 3)

    def test_keys(self):
        keys = list(self.d.keys())
        self.assertEqual(keys[0], "a.b.c.d1")
        self.assertEqual(keys[1], "a.b.c.d2")
        self.assertEqual(keys[2], "a.b.c1")
        self.assertEqual(keys[3], "a.b.c2")
