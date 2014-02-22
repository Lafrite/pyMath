#!/usr/bin/env python
# encoding: utf-8


import unittest

from pymath import arithmetic



class TestArithmetic(unittest.TestCase):
    """Testing functions from pymath.arithmetic"""

    def test_gcd_commu(self):
        self.assertEqual(arithmetic.gcd(3, 15), arithmetic.gcd(15,3))

    def test_gcd1(self):
        self.assertEqual(arithmetic.gcd(3, 15), 3)

    def test_gcd2(self):
        self.assertEqual(arithmetic.gcd(14, 21), 7)

    def test_gcd_prem(self):
        self.assertEqual(arithmetic.gcd(14, 19), 1)

    def test_gcd_neg(self):
        self.assertEqual(arithmetic.gcd(3, -15), 3)
        self.assertEqual(arithmetic.gcd(-3, -15), -3)


if __name__ == '__main__':
    unittest.main()





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

