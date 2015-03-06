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
                1,
                ]

    def test_add(self):
        ans = [[Fraction(2, 3), 1, Fraction(17, 15), 0, 0,  Fraction(4,3)], \
                [Fraction(4,3), Fraction(5,3), Fraction(9,5), Fraction(2,3), Fraction(2,3),  2] \
                ]

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 + f2
                self.assertEqual(res, ans[i][j])

    def test_sub(self):
        ans = [[0, Fraction(-1,3), Fraction(-7, 15), Fraction(2,3), Fraction(2,3), Fraction(-2,3)], \
                [Fraction(2,3), Fraction(1,3), Fraction(1,5), Fraction(4,3), Fraction(4,3), 0] \
                ]

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 - f2
                self.assertEqual(res, ans[i][j])

    def test_neg(self):
        ans = [ Fraction(-1,3), \
            Fraction(-2,3), \
            Fraction(-4,5), \
            Fraction(1, 3), \
            Fraction(1,3), \
            -1
            ]
        for (j, f) in enumerate(self.listAgainst):
            res = -f
            self.assertEqual(res, ans[j])

    def test_mul(self):
        ans = [[Fraction(1, 9), Fraction(2,9), Fraction(4, 15), Fraction(-1,9), Fraction(-1,9), Fraction(1,3)], \
                [ Fraction(1,3), Fraction(2,3), Fraction(4,5), Fraction(-1, 3), Fraction(1,-3), 1] \
                ]

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 * f2
                self.assertEqual(res, ans[i][j])

    def test_truediv(self):
        ans = [[1, Fraction(1,2), Fraction(5, 12), -1, -1, Fraction(1,3)], \
                [3, Fraction(3,2), Fraction(5,4), -3, -3,  1] \
                ]

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 / f2
                self.assertEqual(res, ans[i][j])

    def test_lt(self):
        pass

    def test_le(self):
        pass

    def test_tex(self):
        f = Fraction(2, 3)
        ans = "\\frac{ 2 }{ 3 }"
        self.assertEqual(f.__tex__(), ans)
    
    def test_txt(self):
        f = Fraction(2, 3)
        ans = "2 / 3"
        self.assertEqual(f.__txt__(), ans)

if __name__ == '__main__':
    unittest.main()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
