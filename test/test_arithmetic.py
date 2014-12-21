#!/usr/bin/env python
# encoding: utf-8


from pymath import arithmetic



def test_gcd_commu():
    assert arithmetic.gcd(3, 15) == arithmetic.gcd(15,3)

def test_gcd1():
    assert arithmetic.gcd(3, 15) == 3

def test_gcd2():
    assert arithmetic.gcd(14, 21) == 7

def test_gcd_prem():
    assert arithmetic.gcd(14, 19) == 1

def test_gcd_neg():
    assert arithmetic.gcd(3, -15) == 3
    assert arithmetic.gcd(-3, -15) == -3






# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

