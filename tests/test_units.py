import unittest


class UnitsTest(unittest.TestCase):

    def assertUnitEqual(self, num_l, unit_l, num_r, unit_r):
        self.assertEqual(int(unit_l.convert_to(num_l, unit_r)), int(num_r))
        self.assertEqual(int(unit_l.convert_from(num_r, unit_r)), int(num_l))
        self.assertEqual(int(unit_r.convert_to(num_r, unit_l)), int(num_l))
        self.assertEqual(int(unit_r.convert_from(num_l, unit_l)), int(num_r))

    def testTime(self):
        from zcommons import TimeUnits as T
        self.assertUnitEqual(1, T.MICRO, 1000, T.NANO)
        self.assertUnitEqual(5, T.MILLI, 5000, T.MICRO)
        self.assertUnitEqual(9, T.SECOND, 9000, T.MILLI)
        self.assertUnitEqual(3, T.MINUTE, 180, T.SECOND)
        self.assertUnitEqual(10, T.HOUR, 600, T.MINUTE)

    def testNumber(self):
        from zcommons import NumberUnits as N
        self.assertUnitEqual(1234567890, N.PETA, 12345678900000000000000, N.HECTO)
        self.assertUnitEqual(3, N.PETA, 3000, N.TERA)
        self.assertUnitEqual(2, N.TERA, 2000, N.GIGA)
        self.assertUnitEqual(7, N.GIGA, 7000, N.MEGA)
        self.assertUnitEqual(4, N.MEGA, 4000, N.KILO)
        self.assertUnitEqual(6, N.KILO, 60, N.HECTO)
        self.assertUnitEqual(3, N.HECTO, 30, N.DECA)
        self.assertUnitEqual(3, N.DECA, 30, N.BASE)

    def testBinary(self):
        from zcommons import BinaryUnits as B
        self.assertUnitEqual(8, B.PiB, 64, B.Pib)
        # bytes
        self.assertUnitEqual(5, B.PiB, 5120, B.TiB)
        self.assertUnitEqual(5, B.TiB, 5120, B.GiB)
        self.assertUnitEqual(5, B.GiB, 5120, B.MiB)
        self.assertUnitEqual(5, B.MiB, 5120, B.KiB)
        self.assertUnitEqual(5, B.KiB, 5120, B.B)
        # bits
        self.assertUnitEqual(4, B.Pib, 4096, B.Tib)
        self.assertUnitEqual(4, B.Tib, 4096, B.Gib)
        self.assertUnitEqual(4, B.Gib, 4096, B.Mib)
        self.assertUnitEqual(4, B.Mib, 4096, B.Kib)
        self.assertUnitEqual(4, B.Kib, 4096, B.b)

    def testError(self):
        self.assertRaises(ValueError, zcommons.units.TimeUnits.SECOND.convert_to, 1, "Kib")
        self.assertRaises(TypeError, zcommons.units.TimeUnits.SECOND.convert_to, 1, zcommons.units.NumberUnits.KILO)