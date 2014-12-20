#!/usr/bin/env python
# encoding: utf-8


import unittest

from pymath.polynom import Polynom
from pymath.fraction import Fraction
from pymath.expression import Expression


class TestPolynom(unittest.TestCase):
    """Testing functions from pymath.polynom"""

    def test_init(self):
        p = Polynom([1, 2, 3], "x")

    def test_init_multi(self):
        p = Polynom([1, [2, 3], 4], "x")

    #def test_init_arith(self):
    #    p = Polynom([1, [2, 3, "+"], 4], "x")

    #def test_init_arith_2(self):
    #    p = Polynom([1, [[2, 3, "*"],3], 4], "x")

    def test_deg(self):
        pass

    def test_eval(self):
        pass

    #def test_print(self):
    #    p = Polynom([1,2,3])
    #    ans = "1 + 2 x + 3 x^2"
    #    self.assertEqual(ans, str(p))

    #def test_print_monom(self):
    #    p = Polynom([0,2])
    #    ans = "2 x"
    #    self.assertEqual(ans, str(p))

    #def test_print_0_coef(self):
    #    p = Polynom([0,1,3])
    #    ans = "x + 3 x^2"
    #    self.assertEqual(ans, str(p))

    #def test_print_multi_coef(self):
    #    p = Polynom([1,[2, -2],3])
    #    ans = "1 + 2 x - 2 x + 3 x^2"
    #    self.assertEqual(ans, str(p))

    def test_postfix(self):
        p = Polynom([1,2,3])
        #ans = [1, 2, "x", "*", "+", 3, "x", 2, "^", "*", "+"]
        ans = [3, 'x', 2, '^', '*', 2, 'x', '*', '+', 1, '+']
        self.assertEqual(ans, p.postfix)

    def test_postfix_monom(self):
        p = Polynom([0,2])
        ans = [2, "x", "*"]
        self.assertEqual(ans, p.postfix)

    def test_postfix_0_coef(self):
        p = Polynom([0,2,0,4])
        #ans = [2, "x", "*", 4, "x", 3, "^", "*", "+"]
        ans = [4, 'x', 3, '^', '*', 2, 'x', '*', '+']
        self.assertEqual(ans, p.postfix)

    def test_postfix_1_coef(self):
        p = Polynom([0,1,1])
        #ans = ["x", "x", 2, "^", "+"]
        ans = ["x", 2, "^", "x", "+"]
        self.assertEqual(ans, p.postfix)

    def test_postfix_neg_coef(self):
        # TODO: Choix arbitraire (vis à vis des + et des -) il faudra faire en fonction de render |sam. juin 14 09:45:55 CEST 2014
        p = Polynom([-1,-2,-3])
        #ans = [-1, -2, "x", "*", "+", -3, "x", 2, "^", "*", "+"]
        ans = [-3, 'x', 2, '^', '*', 2, 'x', '*', '-', 1, '-']
        self.assertEqual(ans, p.postfix)

    def test_postfix_multi_coef(self):
        p = Polynom([1,[2, 3],4])
        #ans = [1, 2, "x", "*", "+", 3, "x", "*", "+", 4, "x", 2, "^", "*", "+"]
        ans = [4, 'x', 2, '^', '*', 2, 'x', '*', '+', 3, 'x', '*', '+', 1, '+']
        self.assertEqual(ans, p.postfix)

    def test_postfix_arithm_coef(self):
        p = Polynom([1,Expression([2, 3, "+"]),4])
        #ans = [1, 2, 3, "+", "x", "*", "+", 4, "x", 2, "^", "*", "+"]
        ans = [4, 'x', 2, '^', '*', 2, 3, '+', 'x', '*', '+', 1, '+']
        self.assertEqual(ans, p.postfix)

    #def test_reduce_nilpo(self):
    #    p = Polynom([1, 2, 3])
    #    self.assertEqual(p, p.reduce()[-1])

    def test_reduce(self):
        p = Polynom([1, [2, 3], 4])
        self.assertEqual(str(p.reduce()[-1]),'4 x ^ 2 + 5 x + 1')

    def test_add_int(self):
        p = Polynom([1, 2, 3])
        q = (p + 2)[-1]
        self.assertEqual(str(q), '3 x ^ 2 + 2 x + 3')

    def test_add_frac(self):
        p = Polynom([1, 2, 3])
        f = Fraction(1, 2)
        q = (p + f)[-1]
        #ans = repr(Polynom([Expression(Fraction(3, 2)), Expression(2), Expression(3)]))
        self.assertEqual(str(q),'3 x ^ 2 + 2 x + 3 / 2')

    def test_add_poly(self):
        p = Polynom([1, 0, 3])
        q = Polynom([0, 2, 3])
        r = (p + q)[-1]
        self.assertEqual(str(r), '6 x ^ 2 + 2 x + 1')

    def test_radd_int(self):
        pass

    def test_radd_frac(self):
        pass

    def test_radd_poly(self):
        pass

    def test_mul_int(self):
        pass

    def test_mul_frac(self):
        pass

    def test_mul_poly(self):
        pass

    def test_rmul_int(self):
        pass

    def test_rmul_frac(self):
        pass

    def test_rmul_poly(self):
        pass


if __name__ == '__main__':
    unittest.main()








# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

