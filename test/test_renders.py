#!/usr/bin/env python
# encoding: utf-8


import unittest

from pymath.renders import tex_render, txt_render
from pymath.fraction import Fraction
from pymath.polynom import Polynom



class TestTexRender(unittest.TestCase):
    """Testing functions from pymath.renders.tex_render"""

    def test_type_render_int(self):
        self.assertEqual(tex_render([2]), "2")

    def test_type_render_str(self):
        self.assertEqual(tex_render(["a"]), "a")

    def test_type_render_fraction(self):
        self.assertEqual(tex_render([Fraction(1,2)]), "\\frac{ 1 }{ 2 }")

    def test_type_render_polynom(self):
        self.assertEqual(tex_render([Polynom({"": 1, "x": 3})]), "3x + 1")

    def test_mult_interger(self):
        exps = [ [2, 3, "*"], [2, -3, "*"], [-2, 3, "*"]]
        wanted_render = [ "2 \\times 3", "2 \\times ( -3 )", "-2 \\times 3"]
        for (i,e) in enumerate(exps):
            rend = tex_render(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_letter(self):
        exps = [ [2, "a", "*"], ["a", 3, "*"], [-2, "a", "*"], ["a", -2, "*"]]
        wanted_render = [ "2 a", "a \\times 3", "-2 a", "a \\times ( -2 )"]
        for (i,e) in enumerate(exps):
            rend = tex_render(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_fraction(self):
        exps = [ [2, Fraction(1,2), "*"], [Fraction(1,2), 3, "*"]]
        wanted_render = [ "2 \\times \\frac{ 1 }{ 2 }", "\\frac{ 1 }{ 2 } \\times 3"]
        for (i,e) in enumerate(exps):
            rend = tex_render(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_exp(self):
        pass

    def test_slash(self):
        pass




class TesttxtRender(unittest.TestCase):
    """Testing functions from pymath.renders.txt_render"""

    def test_type_render_int(self):
        self.assertEqual(txt_render([2]), "2")

    def test_type_render_str(self):
        self.assertEqual(txt_render(["a"]), "a")

    def test_type_render_fraction(self):
        self.assertEqual(txt_render([Fraction(1,2)]), "1 / 2")

    def test_type_render_polynom(self):
        self.assertEqual(txt_render([Polynom({"": 1, "x": 3})]), "3x + 1")

    def test_mult_interger(self):
        exps = [ [2, 3, "*"], [2, -3, "*"], [-2, 3, "*"]]
        wanted_render = [ "2 * 3", "2 * ( -3 )", "-2 * 3"]
        for (i,e) in enumerate(exps):
            rend = txt_render(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_letter(self):
        exps = [ [2, "a", "*"], ["a", 3, "*"], [-2, "a", "*"], ["a", -2, "*"]]
        wanted_render = [ "2 a", "a * 3", "-2 a", "a * ( -2 )"]
        for (i,e) in enumerate(exps):
            rend = txt_render(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_fraction(self):
        exps = [ [2, Fraction(1,2), "*"], [Fraction(1,2), 3, "*"]]
        wanted_render = [ "2 * 1 / 2", "1 / 2 * 3"]
        for (i,e) in enumerate(exps):
            rend = txt_render(e)
            self.assertEqual(rend, wanted_render[i])

    def test_mult_exp(self):
        pass

    def test_slash(self):
        pass


if __name__ == '__main__':
    unittest.main()








# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

