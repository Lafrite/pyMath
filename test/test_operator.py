#!/usr/bin/env python
# encoding: utf-8

from pymath.operator import op


def test_mul_is_visible():
    assert op.mul.is_visible(2,3) == True
    assert op.mul.is_visible(2,-3) == True
    assert op.mul.is_visible(-2,3) == True
    assert op.mul.is_visible('a',2) == True
    assert op.mul.is_visible('2a + 1', 2) == True
    assert op.mul.is_visible(2, '(-2)') == True
    assert op.mul.is_visible(2, '2a') == True
    assert op.mul.is_visible(2, '(-2a)') == True
    assert op.mul.is_visible(2, '(-2abc)') == True

    assert op.mul.is_visible(2,'a') == False
    assert op.mul.is_visible(2, '(2a + 1)') == False
    assert op.mul.is_visible('(3x - 1)', '(2a + 1)') == False
    assert op.mul.is_visible(2, '(-2x + 1)(3x + 2)') == False







# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

