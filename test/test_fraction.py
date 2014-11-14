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
        # TODO: Bug pour 1 + 1/-3 |sam. févr. 22 07:01:29 CET 2014

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 + f2

                #print("-----------")
                #print("f1 : ", f1)
                #print("f2 : ", f2)
                #print(res)

                # On est obligé de faire ça pour gérer le cas de 1+1 qui ne passe pas par la classe Fraction
                if type(res) == list:
                    self.assertEqual(res[-1], ans[i][j])
                else:
                    self.assertEqual(res, ans[i][j])

    def test_sub(self):
        ans = [[0, Fraction(-1,3), Fraction(-7, 15), Fraction(2,3), Fraction(2,3), Fraction(-2,3)], \
                [Fraction(2,3), Fraction(1,3), Fraction(1,5), Fraction(4,3), Fraction(4,3), 0] \
                ]
        # TODO: bug pour 1 - 1/-3 |sam. févr. 22 07:05:15 CET 2014

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 - f2

                #print("-----------")
                #print("f1 : ", f1)
                #print("f2 : ", f2)
                #print(res)

                # On est obligé de faire ça pour gérer le cas de 1-1 qui ne passe pas par la classe Fraction
                if type(res) == list:
                    self.assertEqual(res[-1], ans[i][j])
                else:
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
            if type(res) == list:
                self.assertEqual(res[-1], ans[j])
            else:
                self.assertEqual(res, ans[j])

    def test_mul(self):
        ans = [[Fraction(1, 9), Fraction(2,9), Fraction(4, 15), Fraction(-1,9), Fraction(-1,9), Fraction(1,3)], \
                [ Fraction(1,3), Fraction(2,3), Fraction(4,5), Fraction(-1, 3), Fraction(1,-3), 1] \
                ]

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 * f2

                #print("-----------")
                #print("f1 : ", f1)
                #print("f2 : ", f2)
                #print(res)

                # On est obligé de faire ça pour gérer le cas de 1*1 qui ne passe pas par la classe Fraction
                if type(res) == list:
                    self.assertEqual(res[-1], ans[i][j])
                else:
                    self.assertEqual(res, ans[i][j])

    def test_truediv(self):
        ans = [[1, Fraction(1,2), Fraction(5, 12), -1, -1, Fraction(1,3)], \
                [3, Fraction(3,2), Fraction(5,4), -3, -3,  1] \
                ]

        for (i, f1) in enumerate(self.listFrom):
            for (j, f2) in enumerate(self.listAgainst):
                res = f1 / f2

                #print("-----------")
                #print("f1 : ", f1)
                #print("f2 : ", f2)
                #print(res)

                # On est obligé de faire ça pour gérer le cas de 1/1 qui ne passe pas par la classe Fraction
                if type(res) == list:
                    self.assertEqual(res[-1], ans[i][j])
                else:
                    self.assertEqual(res, ans[i][j])

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
