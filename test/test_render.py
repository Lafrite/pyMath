#!/usr/bin/env python
# encoding: utf-8


import unittest

from pymath.render import tex, txt,p2i
from pymath.fraction import Fraction
from pymath.operator import op



class TestTexRender(unittest.TestCase):
    """Testing functions from pymath.renders.tex"""

    def test_type_render_int(self):
        self.assertEqual(tex([2]), "2")

    def test_type_render_str(self):
        self.assertEqual(tex(["a"]), "a")

    def test_type_render_fraction(self):
        self.assertEqual(tex([Fraction(1,2)]), "\\frac{ 1 }{ 2 }")

    def test_mult_interger(self):
        exps = [ [2, 3, op.get_op("*", 2)], [2, -3, op.get_op("*", 2)], [-2, 3, op.get_op("*", 2)]]
        wanted_render = [ "2 \\times 3", "2 \\times ( -3 )", "-2 \\times 3"]
        for (i,e) in enumerate(exps):
            rend = tex(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_letter(self):
        exps = [ [2, "a", op.get_op("*", 2)], ["a", 3, op.get_op("*", 2)], [-2, "a", op.get_op("*", 2)], ["a", -2, op.get_op("*", 2)]]
        wanted_render = [ "2 a", "a \\times 3", "-2 a", "a \\times ( -2 )"]
        for (i,e) in enumerate(exps):
            rend = tex(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_fraction(self):
        exps = [ [2, Fraction(1,2), op.get_op("*", 2)], [Fraction(1,2), 3, op.get_op("*", 2)]]
        wanted_render = [ "2 \\times \\frac{ 1 }{ 2 }", "\\frac{ 1 }{ 2 } \\times 3"]
        for (i,e) in enumerate(exps):
            rend = tex(e)
            self.assertEqual(rend, wanted_render[i])

    def test_parentheses(self):
        mul = op.get_op("*", 2)
        add = op.get_op("+", 2)
        exps = [\
            [ 2, 3, add, 4, mul],\
            [ 2, 3, mul, 4, add],\
            [ 2, 3, 4, mul, add],\
            [ 2, 3, 4, add, add],\
            ]
        wanted_render = [\
                '( 2 + 3 ) \\times 4',\
                '2 \\times 3 + 4',\
                '2 + 3 \\times 4',\
                '2 + 3 + 4',\
                ]
        for (i,e) in enumerate(exps):
            rend = tex(e)
            self.assertEqual(rend, wanted_render[i])

    def test_slash(self):
        pass




class TesttxtRender(unittest.TestCase):
    """Testing functions from pymath.renders.txt"""

    def test_type_render_int(self):
        self.assertEqual(txt([2]), "2")

    def test_type_render_str(self):
        self.assertEqual(txt(["a"]), "a")

    def test_type_render_fraction(self):
        self.assertEqual(txt([Fraction(1,2)]), "1 / 2")

    def test_mult_interger(self):
        exps = [ [2, 3, op.get_op("*", 2)], \
                [2, -3, op.get_op("*", 2)], \
                [-2, 3, op.get_op("*", 2)]]
        wanted_render = [ "2 * 3", "2 * ( -3 )", "-2 * 3"]
        for (i,e) in enumerate(exps):
            rend = txt(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_letter(self):
        exps = [ [2, "a", op.get_op("*", 2)], \
                ["a", 3, op.get_op("*", 2)], \
                [-2, "a", op.get_op("*", 2)], \
                ["a", -2, op.get_op("*", 2)]]
        wanted_render = [ "2 a", "a * 3", "-2 a", "a * ( -2 )"]
        for (i,e) in enumerate(exps):
            rend = txt(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_fraction(self):
        exps = [ [2, Fraction(1,2), op.get_op("*", 2)], \
                [Fraction(1,2), 3, op.get_op("*", 2)]]
        wanted_render = [ "2 * 1 / 2", "1 / 2 * 3"]
        for (i,e) in enumerate(exps):
            rend = txt(e)
            self.assertEqual(rend, wanted_render[i])

    def test_parentheses(self):
        mul = op.get_op("*", 2)
        add = op.get_op("+", 2)
        exps = [\
            [ 2, 3, add, 4, mul],\
            [ 2, 3, mul, 4, add],\
            [ 2, 3, 4, mul, add],\
            [ 2, 3, 4, add, add],\
            ]
        wanted_render = [\
                '( 2 + 3 ) * 4',\
                '2 * 3 + 4',\
                '2 + 3 * 4',\
                '2 + 3 + 4',\
                ]
        for (i,e) in enumerate(exps):
            rend = txt(e)
            self.assertEqual(rend, wanted_render[i])

    def test_slash(self):
        pass


if __name__ == '__main__':
    unittest.main()








# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

