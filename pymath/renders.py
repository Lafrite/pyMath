#!/usr/bin/env python
# encoding: utf-8

from .render import Render
from .fraction import Fraction
from .polynom import Polynom
from .generic import first_elem, last_elem

# ------------------------
# A infix to postfix list convertor

p2i_infix = {"+": "+", "-": "-", "*": "*", "/" : "/", ":": ":", "^":"^"}
p2i_postfix = {}
p2i_other = {"(": "(", ")": ")"}

post2in_fix = Render(p2i_infix, p2i_postfix, p2i_other, join = False)

# ------------------------
# A console render

def txtMult(op1,op2):
    """ Tex render for *
    Cases where \\times won't be displayed
        * nbr  letter 
        * nbr  (
        * )(
    """
    first_nbr = type(op1) in [int, Fraction]
    seg_letter = type(op2) == str and op2.isalpha()
    first_par = (first_elem(op2) == "(")
    seg_par = (last_elem(op1) == ")")

    if (first_nbr and (seg_letter or seg_par)) \
            or (first_par and seg_par):
        return [op1, op2]
    else:
        return [op1, "*", op2]

txt_infix = {"+": "+", "-": "-", "*": txtMult, "/" : "/", ":":":", "^":"^"}
txt_postfix = {}
txt_other = {"(": "(", ")": ")"}

txt_render = Render(txt_infix, txt_postfix, txt_other)

# ------------------------
# A latex render

def texSlash(op1, op2):
    """ Tex render for / """
    if not Render.isNumerande(op1) and op1[0] == "(" and op1[-1] == ")":
        op1 = op1[1:-1]
    if not Render.isNumerande(op2) and op2[0] == "(" and op2[-1] == ")":
        op2 = op2[1:-1]
    return ["\\frac{" , op1 , "}{" , op2 , "}"]

def texFrac(frac):
    """ Tex render for Fractions"""
    return ["\\frac{" , str(frac._num) , "}{" , str(frac._denom) , "}"]

def texMult(op1,op2):
    """ Tex render for *
    Cases where \\times won't be displayed
        * nbr  letter 
        * nbr  (
        * )(
    """
    first_nbr = type(op1) in [int, Fraction]
    seg_letter = type(op2) == str and op2.isalpha()
    first_par = (first_elem(op2) == "(")
    seg_par = (last_elem(op1) == ")")

    if (first_nbr and (seg_letter or seg_par)) \
            or (first_par and seg_par):
        return [op1, op2]
    else:
        return [op1, "\\times", op2]

tex_infix = {"+": " + ", "-": " - ", "*": texMult , ":": ":", "^":"^"}
tex_postfix = {"/": texSlash}
tex_other = {"(": "(", ")": ")"}
tex_type_render = {str:str, int: str, Fraction: texFrac, Polynom: str}

tex_render = Render(tex_infix, tex_postfix, tex_other, type_render = tex_type_render)



if __name__ == '__main__':
    #exp = [2, 5, '^', 1, '-', 3, 4, '*', ':']
    #print(txt_render(exp))
    #exp = [2, 5, '^', 1, '-', 3, 4, '*', '/', 3, 5, '/', ':']
    exp = [2, -3, "*"]
    print(tex_render(exp))
    #exp = [2, 5, '^', 1, '-', 3, 4, '*', '/', 3, '+']
    #print(post2in_fix(exp))




# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
