#!/usr/bin/env python
# encoding: utf-8



import unittest

from pymath.expression import Expression
from pymath.fraction import Fraction
from pymath.generic import first_elem
from pymath.renders import txt_render


class TestExpression(unittest.TestCase):
    """Testing functions from pymath.expression"""

    def test_init_from_str(self):
        exp = Expression("2 + 3")
        self.assertEqual(exp.infix_tokens, [2, "+", 3])
        self.assertEqual(exp.postfix_tokens, [2, 3, "+"])

    def test_init_from_exp(self):
        pass

    def test_infix_tokens(self):
        pass

    def test_postfix_tokens(self):
        pass

    def test_str2tokens_big_num(self):
        exp = "123 + 3"
        tok = Expression.str2tokens(exp)
        self.assertEqual(tok, [123, "+", 3])

    def test_str2tokens_beg_minus(self):
        exp = "-123 + 3"
        tok = Expression.str2tokens(exp)
        self.assertEqual(tok, [-123, "+", 3])

    def test_str2tokens_time_lack(self):
        exp = "(-3)(2)"
        tok = Expression.str2tokens(exp)
        self.assertEqual(tok, ["(", -3, ")", "*","(", 2, ")" ])

    def test_str2tokens_time_lack2(self):
        exp = "-3(2)"
        tok = Expression.str2tokens(exp)
        self.assertEqual(tok, [-3, "*","(", 2, ")" ])

    def test_str2tokens_error_float(self):
        exp = "1 + 1.3"
        self.assertRaises(ValueError, Expression.str2tokens, exp)

    def test_str2tokens_error(self):
        exp = "1 + $"
        self.assertRaises(ValueError, Expression.str2tokens, exp)

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

    def test_simplify_frac(self):
        exp = Expression("1/2 - 4")
        steps = ["[1, 2, '/', 4, '-']", \
                "[< Fraction 1 / 2>, 4, '-']", \
                "[1, 1, '*', 2, 1, '*', '/', 4, 2, '*', 1, 2, '*', '/', '-']", \
                "[1, 8, '-', 2, '/']", \
                '[< Fraction -7 / 2>]']
        self.assertEqual(steps, list(exp.simplify()))


if __name__ == '__main__':
    unittest.main()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
