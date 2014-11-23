#!/usr/bin/env python
# encoding: utf-8


import unittest

from pymath.random_expression import RdExpression


class TestRandomExpression(unittest.TestCase):
    """Testing functions from pymath.random_expression"""

    def test_only_form(self):
        form = "{a} + 2"
        rdExp = RdExpression(form)

        self.assertEqual(rdExp._letters, {'a'})
        self.assertEqual(rdExp._2replaced, {'a'})

        rdExp()
        self.assertEqual(set(rdExp._gene_varia.keys()), {'a'}) 
        self.assertEqual(set(rdExp._gene_2replaced.keys()), {'a'}) 

    def test_only_form_calc(self):
        form = "{a + b} + 2"
        rdExp = RdExpression(form)

        self.assertEqual(rdExp._letters, {'a', 'b'})
        self.assertEqual(rdExp._2replaced, {'a + b'})

        rdExp()
        self.assertEqual(set(rdExp._gene_varia.keys()), {'a', 'b'}) 
        self.assertEqual(set(rdExp._gene_2replaced.keys()), {'a + b'}) 

    def test_only_form_cond(self):
        form = "{a} + 2"
        cond = ["{a} == 3"]
        rdExp = RdExpression(form, cond)

        self.assertEqual(rdExp._letters, {'a'})
        self.assertEqual(rdExp._2replaced, {'a'})

        rdExp()
        self.assertEqual(set(rdExp._gene_varia.keys()), {'a'}) 
        self.assertEqual(set(rdExp._gene_2replaced.keys()), {'a'}) 

        self.assertEqual(rdExp._gene_varia['a'], 3)

    def test_only_form_conds(self):
        form = "{a} + 2"
        cond = ["{a} in list(range(5))", "{a} % 2 == 1"]
        rdExp = RdExpression(form, cond)

        self.assertEqual(rdExp._letters, {'a'})
        self.assertEqual(rdExp._2replaced, {'a'})

        rdExp()
        self.assertEqual(set(rdExp._gene_varia.keys()), {'a'}) 
        self.assertEqual(set(rdExp._gene_2replaced.keys()), {'a'}) 

        self.assertTrue(rdExp._gene_varia['a'] in list(range(5)))
        self.assertTrue(rdExp._gene_varia['a'] % 2 == 1)

    def test_only_form_calc_cond(self):
        form = "{a*3} * {b}"
        cond = ["{a} == 3"]
        rdExp = RdExpression(form, cond)

        self.assertEqual(rdExp._letters, {'a', 'b'})
        self.assertEqual(rdExp._2replaced, {'a', 'b', 'a*3'})

        rdExp()
        self.assertEqual(set(rdExp._gene_varia.keys()), {'a', 'b'}) 
        self.assertEqual(set(rdExp._gene_2replaced.keys()), {'a', 'b', 'a*3'}) 

        self.assertEqual(rdExp._gene_varia['a'], 3)


    def test_only_form_calc_cond_calc(self):
        form = "{a*3} * {b}"
        cond = ["{a + b} == 3"]
        rdExp = RdExpression(form, cond)

        self.assertEqual(rdExp._letters, {'a', 'b'})
        self.assertEqual(rdExp._2replaced, {'b', 'a*3', 'a + b'})

        rdExp()
        self.assertEqual(set(rdExp._gene_varia.keys()), {'a', 'b'}) 
        self.assertEqual(set(rdExp._gene_2replaced.keys()), {'b', 'a*3', 'a + b'}) 

        self.assertEqual((rdExp._gene_varia['a'] + rdExp._gene_varia['b']), 3)



if __name__ == '__main__':
    unittest.main()








# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

