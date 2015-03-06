#!/usr/bin/env python
# encoding: utf-8

""" Testing Expression """


from pymath.expression import Expression
from pymath.fraction import Fraction
from pymath.generic import first_elem
from pymath.render import txt, tex


def test_init_from_str():
        exp = Expression("2 + 3")
        assert exp.postfix_tokens == [2, 3, "+"]

def test_init_from_exp():
    pass

def test_init_list():
    exp = Expression([2, 3, "+"])
    assert exp.postfix_tokens == [2, 3, "+"]

def test_init_one_element_int_from_str():
    exp = Expression("1")

def test_init_one_element_int_from_list():
    exp = Expression([1])

#def test_init_one_element_str_from_str():
#    exp = Expression("x")
#
#def test_init_one_element_str_from_list():
#    exp = Expression(["x"])

def test_simplify_exp():
    exp = Expression("1 + 2 * 3")
    simplified = exp.simplify()
    ans = Expression("7")
    assert ans == simplified

#def test_simplify_frac():
#    exp = Expression("1/2 - 4")
#    simplified = exp.simplify()
#    ans = Expression("-7/2")
#    assert simplified == ans
#
#def test_explain_frac():
#    exp = Expression("1/2 - 4")
#    simplified = exp.simplify()
#
#    steps = ['\\frac{ 1 }{ 2 } - 4', \
#        '\\frac{ 1 \\times 1 }{ 2 \\times 1 } - \\frac{ 4 \\times 2 }{ 1 \\times 2 }',\
#        '\\frac{ 1 }{ 2 } - \\frac{ 8 }{ 2 }',\
#        '\\frac{ 1 - 8 }{ 2 }',\
#        '\\frac{ -7 }{ 2 }']
#    assert simplified.steps == list(exp.simplify())

def test_add_exp():
    e = Expression("12- 4")
    f = Expression("4 + 1")
    g = e + f
    assert g.postfix_tokens == [12, 4, '-', 4, 1, "+", "+"]

def test_mul_exp():
    e = Expression("12- 4")
    f = Expression("4 + 1")
    g = e * f
    assert g.postfix_tokens == [12, 4, '-', 4, 1, "+", "*"]

def test_neg_exp():
    e = Expression("12- 4")
    g = -e 
    assert g.postfix_tokens == [12, 4, '-', '-']


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
