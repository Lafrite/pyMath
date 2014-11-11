#!/usr/bin/env python
# encoding: utf-8



import unittest

from pymath.expression import Expression
from pymath.fraction import Fraction
from pymath.generic import first_elem
from pymath.render import txt, tex


class TestExpression(unittest.TestCase):
    """Testing functions from pymath.expression"""

    def test_init_from_str(self):
        exp = Expression("2 + 3")
        self.assertEqual(exp.postfix_tokens, [2, 3, "+"])

    def test_init_from_exp(self):
        pass

    def test_infix_tokens(self):
        pass

    def test_postfix_tokens(self):
        pass


    def test_isNumber(self):
        pass

    def test_isOperator(self):
        pass

    def test_simplify_frac(self):
        exp = Expression("1/2 - 4")
        Expression.STR_RENDER = lambda _,x : str(x)
        steps = ["[1, 2, '/', 4, '-']", \
                "[< Fraction 1 / 2>, 4, '-']", \
                "[1, 1, '*', 2, 1, '*', '/', 4, 2, '*', 1, 2, '*', '/', '-']", \
                "[1, 8, '-', 2, '/']", \
                '[< Fraction -7 / 2>]']
        self.assertEqual(steps, list(exp.simplify()))

        Expression.STR_RENDER = tex


if __name__ == '__main__':
    unittest.main()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
