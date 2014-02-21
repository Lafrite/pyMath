#!/usr/bin/env python
# encoding: utf-8

import unittest

from pymath.fraction import Fraction

class TestFraction(unittest.TestCase):
    """Testing functions from pymath.Fraction"""

    def setUp(self):
        self.listFrom = [Fraction(1,3), 1]
        self.listAgainst = [ Fraction(1,3), \
                Fraction(2,3), \
                Fraction(4,5), \
                Fraction(-1, 3), \
                Fraction(1,-3), \
                Fraction(0,2), \
                1,
                ]

    def test_add(self):
        ans = [[Fraction(2, 3), 1, Fraction(17, 15), 0, 0, Fraction(1,3), Fraction(4,3)], \
                [Fraction(4,3), Fraction(5,3), Fraction(9,3), Fraction(2,3), Fraction(2,3), 1, 0] \
                ]

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 + f2
                print(res)
                self.assertAlmostEqual(res[-1], ans[i][j])


    def test_radd(self):
        pass

    def test_sub(self):
        pass

    def test_rsub(self):
        pass

    def test_neg(self):
        pass

    def test_mul(self):
        pass

    def test_truediv(self):
        pass

    def test_lt(self):
        pass

    def test_le(self):
        pass


if __name__ == '__main__':
    unittest.main()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
