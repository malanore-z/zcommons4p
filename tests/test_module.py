import os
import unittest

import zcommons as zc


class ModuleTest(unittest.TestCase):

    def setUp(self) -> None:
        self.testspath = os.path.dirname(os.path.abspath(__file__))

    def test_import_module(self):
        mod = zc.module.import_module("import_test.sub", path=self.testspath)
        self.assertTrue(hasattr(mod, "Outer"))

    def test_import_object(self):
        sub = zc.module.import_module("import_test.sub", path=self.testspath)
        Inner = zc.module.import_object(".Outer.Inner", package=sub.__name__)
        inner = Inner()
        self.assertTrue(inner.check())
