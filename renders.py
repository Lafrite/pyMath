#!/usr/bin/env python
# encoding: utf-8

from render import Render
from fraction import Fraction
from formal import FormalExp

# ------------------------
# A console render

txt_infix = {"+": "+", "-": "-", "*": "*", "/" : "/", ":": ":"}
txt_postfix = {}
txt_other = {"(": "(", ")": ")"}

txt_render = Render(txt_infix, txt_postfix, txt_other)

# ------------------------
# A infix to postfix list convertor

p2i_infix = {"+": "+", "-": "-", "*": "*", "/" : "/", ":":":"}
p2i_postfix = {}
p2i_other = {"(": "(", ")": ")"}

post2in_fix = Render(p2i_infix, p2i_postfix, p2i_other, join = False)

# ------------------------
# A latex render

def texSlash(op1, op2):
    if not Render.isNumerande(op1) and op1[0] == "(" and op1[-1] == ")":
        op1 = op1[1:-1]
    if not Render.isNumerande(op2) and op2[0] == "(" and op2[-1] == ")":
        op2 = op2[1:-1]
    return ["\\frac{" , op1 , "}{" , op2 , "}"]

def texFrac(frac):
    return ["\\frac{" , str(frac._num) , "}{" , str(frac._denom) , "}"]

tex_infix = {"+": " + ", "-": " - ", "*": " \\times ", ":": ":"}
tex_postfix = {"/": texSlash}
tex_other = {"(": "(", ")": ")"}
tex_type_render = {int: str, Fraction: texFrac, FormalExp: str}

tex_render = Render(tex_infix, tex_postfix, tex_other, type_render = tex_type_render)



if __name__ == '__main__':
    exp = [2, 5, '+', 1, '-', 3, 4, '*', ':']
    print(txt_render(exp))
    exp = [2, 5, '+', 1, '-', 3, 4, '*', '/', 3, 5, '/', ':']
    print(tex_render(exp))
    exp = [2, 5, '+', 1, '-', 3, 4, '*', '/', 3, '+']
    print(post2in_fix(exp))




# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
