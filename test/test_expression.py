#!/usr/bin/env python
# encoding: utf-8



import unittest

from pymath.expression import Expression
from pymath.fraction import Fraction
from pymath.generic import first_elem
from pymath.render import txt, tex


Expression.set_render(txt)

class TestExpression(unittest.TestCase):
    """Testing functions from pymath.expression"""

    def test_init_from_str(self):
        exp = Expression("2 + 3")
        self.assertEqual(exp.postfix_tokens, [2, 3, "+"])

    def test_init_from_exp(self):
        pass

    def test_list(self):
        exp = Expression([2, 3, "+"])
        self.assertEqual(exp.postfix_tokens, [2, 3, "+"])

    def test_simplify_frac(self):
        render = lambda _,x : str(x)
        Expression.set_render(render)
        exp = Expression("1/2 - 4")
        steps = ["[1, 2, '/', 4, '-']", \
                "[< Fraction 1 / 2>, 4, '-']", \
                "[1, 1, '*', 2, 1, '*', '/', 4, 2, '*', 1, 2, '*', '/', '-']", \
                "[1, 8, '-', 2, '/']", \
                '[< Fraction -7 / 2>]']
        self.assertEqual(steps, list(exp.simplify()))
        Expression.set_render(txt)

    def test_add_exp(self):
        e = Expression("12- 4")
        f = Expression("4 + 1")
        g = e + f
        self.assertEqual(g.postfix_tokens, [12, 4, '-', 4, 1, "+", "+"])

    def test_mul_exp(self):
        e = Expression("12- 4")
        f = Expression("4 + 1")
        g = e * f
        self.assertEqual(g.postfix_tokens, [12, 4, '-', 4, 1, "+", "*"])

    def test_neg_exp(self):
        e = Expression("12- 4")
        g = -e 
        self.assertEqual(g.postfix_tokens, [12, 4, '-', '-'])


if __name__ == '__main__':
    unittest.main()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
