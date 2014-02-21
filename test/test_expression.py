#!/usr/bin/env python
# encoding: utf-8



import unittest

from pymath.expression import Expression
from pymath.fraction import Fraction
from pymath.generic import first_elem


class TestExpression(unittest.TestCase):
    """Testing functions from pymath.expression"""

    def test_init_from_exp(self):
        pass

    def test_init_from_exp(self):
        pass

    def test_infix_tokens(self):
        pass

    def test_postfix_tokens(self):
        pass

    def test_doMath(self):
        ops = [\
                {"op": ("+", 1 , 2), "res" : 3}, \
                {"op": ("-", 1 , 2), "res" : -1}, \
                {"op": ("*", 1 , 2), "res" : 2}, \
                {"op": ("/", 1 , 2), "res" : Fraction(1,2)}, \
                {"op": ("^", 1 , 2), "res" : 1}, \
                ]
        for op in ops:
            res = first_elem(Expression.doMath(*op["op"]))
            self.assertAlmostEqual(res, op["res"])

    def test_isNumber(self):
        pass

    def test_isOperator(self):
        pass

if __name__ == '__main__':
    unittest.main()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
