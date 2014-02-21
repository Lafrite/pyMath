#!/usr/bin/env python
# encoding: utf-8


import unittest

from pymath import generic

class TestGeneric(unittest.TestCase):
    """Testing functions from pymath.generic"""

    def test_flatten_list1(self):
        l = [1, [2,3], [[4,5], 6], 7]
        flat_l = generic.flatten_list(l)

        true_flat = list(range(1,8))

        self.assertEqual(flat_l, true_flat)

    def test_flatten_list2(self):
        l = list(range(10))
        flat_l = generic.flatten_list(l)

        true_flat = list(range(10))

        self.assertEqual(flat_l, true_flat)

    def test_first_elem_simple_iter(self):
        """ For simple iterable """
        l = range(10)
        first = generic.first_elem(l)

        self.assertAlmostEqual(0,first)

        s = "plopplop"
        first = generic.first_elem(s)
        self.assertAlmostEqual("p", first)

    def test_first_elem_iter_in_iter(self):
        """ Interable in iterable """
        l = [[1,2],[4, 5, [6,7,8]], 9]
        first = generic.first_elem(l)

        self.assertAlmostEqual(first, 1)

        l = [[[1]]]
        first = generic.first_elem(l)

        self.assertAlmostEqual(first, 1)

        l = ["abc"]
        first = generic.first_elem(l)

        self.assertAlmostEqual(first, "a")

        l = ["abc",[4, 5, [6,7,8]], 9]
        first = generic.first_elem(l)

        self.assertAlmostEqual(first, "a")

        l = [["abc",1],[4, 5, [6,7,8]], 9]
        first = generic.first_elem(l)

        self.assertAlmostEqual(first, "a")

if __name__ == '__main__':
    unittest.main()

        



# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
