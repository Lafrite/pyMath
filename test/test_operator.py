#!/usr/bin/env python
# encoding: utf-8

from pymath.operator import op


# Test de op.add

def test_add_render_tex():
    assert op.add.__tex__('1','2') == '1 + 2'
    assert op.add.__tex__('1','-2') == '1 - 2'

def test_add_render_txt():
    assert op.add.__txt__('1','2') == '1 + 2'
    assert op.add.__txt__('1','-2') == '1 - 2'

# Test de op.sub

def test_sub_render_tex():
    assert op.sub.__tex__('1','2') == '1 - 2'
    assert op.sub.__tex__('1','-2') == '1 - ( -2 )'

def test_sub_render_txt():
    assert op.sub.__txt__('1','2') == '1 - 2'
    assert op.sub.__txt__('1','-2') == '1 - ( -2 )'

# Test de op.sub1

def test_sub1_render():
    assert op.sub1.__tex__('1') == '- 1'
    assert op.sub1.__tex__('-1') == '- ( -1 )'
    assert op.sub1.__txt__('1') == '- 1'
    assert op.sub1.__txt__('-1') == '- ( -1 )'

# Test de op.mul
def test_mul_render_tex():
    assert op.mul.__tex__('1','2') == '1 \\times 2'
    assert op.mul.__tex__('1','-2') == '1 \\times ( -2 )'

def test_mul_render_txt():
    assert op.mul.__txt__('1','2') == '1 * 2'
    assert op.mul.__txt__('1','-2') == '1 * ( -2 )'

def test_mul_is_visible():
    assert op.mul.is_visible(2,3) == True
    assert op.mul.is_visible(2,-3) == True
    assert op.mul.is_visible(-2,3) == True
    assert op.mul.is_visible('a',2) == True
    assert op.mul.is_visible('(2a + 1)', 2) == True
    assert op.mul.is_visible(2, '(-2)') == True
    assert op.mul.is_visible(2, '2a') == True
    assert op.mul.is_visible(2, '(-2a)') == True
    assert op.mul.is_visible(2, '(-2abc)') == True

    assert op.mul.is_visible(2,'a') == False
    assert op.mul.is_visible(2, '(2a + 1)') == False
    assert op.mul.is_visible('(3x - 1)', '(2a + 1)') == False
    assert op.mul.is_visible(2, '(-2x + 1)(3x + 2)') == False

# Test de op.div
def test_div_render_tex():
    assert op.div.__tex__('1','2') == '\\frac{ 1 }{ 2 }'
    assert op.div.__tex__('1','-2') == '\\frac{ 1 }{ -2 }'

def test_div_render_txt():
    assert op.div.__txt__('1','2') == '1 / 2'
    assert op.div.__txt__('1','-2') == '1 / ( -2 )'

# Test de op.pw
def test_pw_render_tex():
    assert op.pw.__tex__('1','2') == '1^{  2 }'
    assert op.pw.__tex__('1','-2') == '1^{-2}'
    assert op.pw.__tex__('-1','2') == '( -1 )^{ 2 }'

def test_pw_render_txt():
    assert op.pw.__txt__('1','2') == '1 ^ 2'
    assert op.pw.__txt__('1','-2') == '1 ^ ( -2 )'
    assert op.pw.__txt__('-1','2') == '( -1 ) ^ 2 '





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

