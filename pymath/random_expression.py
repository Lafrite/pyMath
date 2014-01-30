#!/usr/bin/env python
# encoding: utf-8

from random import randint
from .expression import Expression
from .renders import tex_render, txt_render
import re

class RdExpression(object):
    """A generator of random expression builder"""

    def __init__(self, form, conditions = [], with_Exp = True):
        """Initiate the generator

        :param form: the form of the expression (/!\ variables need to be in brackets {})
        :param conditions: condition on variables (/!\ variables need to be in brackets {})
        :param with_Exp: If True, __call__ return an expression rendered through Expression class. If False, keep form and replace inside.

        """
        self._form = form
        self._conditions = conditions
        self._with_Exp = with_Exp
        self._letters = self.get_letters()
        self._gene_varia = {}
        self._gene_2replaced= {}

    def get_2replaced(self):
        """Get elements of self._form which will have to be replaced
        :returns: set for elements which have to be replaced

        """
        pattern = "\{(.*?)\}" #select inside {} non greedy way
        varia = re.findall(pattern, self._form)
        varia = set(varia)
        self._2replaced = varia

        return varia
        
    def get_letters(self):
        """Find letters in the form
        :returns: list of letters

        """
        v2replaced = self.get_2replaced()
        varia = set()

        pattern = "([a-zA-Z]+)"
        for v in v2replaced:
            lvar = set(re.findall(pattern, v))
            varia = varia | lvar

        return varia


    def __call__(self, val_min = -10, val_max = 10, render = tex_render):
        """RdExpression once it is initiate act like a function which create random expressions.

        :param val_min: minimum value random generation
        :param val_max: maximum value random generation
        :param render: Render of the expression (returns an Expression by default)
        :returns: an formated random expression 

        """
        if self._with_Exp:
            return render(self.raw_exp(val_min, val_max).postfix_tokens)
        else:
            return self.raw_str(val_min, val_max)

    def raw_str(self, val_min = -10, val_max = 10):
        """Return raw string (don't use Expression for rendering or parsing)

        :param val_min: minimum value random generation
        :param val_max: maximum value random generation
        :returns: an random Expression object

        """
        self.gene_varia(val_min, val_max)

        while not(self.val_conditions()):
            self.gene_varia(val_min, val_max)

        exp = self._form.format(**self._gene_2replaced)

        return exp

    def raw_exp(self, val_min = -10, val_max = 10):
        """Same as raw_str but returns an Expression object

        :param val_min: minimum value random generation
        :param val_max: maximum value random generation
        :returns: an random Expression object

        """
        exp = self.raw_str(val_min, val_max)

        return Expression(exp)

    def gene_varia(self, val_min = -10, val_max = 10):
        """RAndomly generates variables/letters

        """
        for l in self._letters:
            self._gene_varia[l] = randint(val_min, val_max)
            while self._gene_varia[l] == 0:
                self._gene_varia[l] = randint(val_min, val_max)

        for e in self._2replaced:
            self._gene_2replaced[e] = eval(e, globals(), self._gene_varia)

    def val_conditions(self):
        """Tells whether or not conditions are validates
        :returns: boolean

        """
        if self._conditions != []:
            return eval(" and ".join(self._conditions).format(**self._gene_varia))
        else:
            return True

def desc_rdExp(rdExp):
    print("--------------------")
    print("form: ",rdExp._form)
    print("Conditions: ",rdExp._conditions)
    print("Letters: ", rdExp._letters)
    print("2replaced: ", rdExp._2replaced)
    print("Call : ", rdExp(render = tex_render))
    print("Gene varia: ", rdExp._gene_varia)
    print("Gene 2replaced: ", rdExp._gene_2replaced)
    print('')


if __name__ == '__main__':
    #form = "{a}*-14 / (2*{b}) : -23 / 4"
    #cond = ["{a} + {b} in [1, 2, 3, 4, 5]", "{a} not in [0,1]", "{b} not in [0,1]"]
    #rdExp1 = RdExpression(form, cond)
    #desc_rdExp(rdExp1)
    #rdExp2 = RdExpression(form)
    #desc_rdExp(rdExp2)
    #form = "{a+a/10}x + {a} + 2*{b}"
    #cond = ["{a} + {b} in [1, 2, 3, 4, 5]", "{a} not in [0,1]", "{b} not in [0,1]"]
    #rdExp3 = RdExpression(form)
    #desc_rdExp(rdExp3)

    form1 = "{a**2}x^2 + {2*a*b}x + {b**2}"
    cond1 = []
    rdExp1 = RdExpression(form1, cond1, with_Exp = False)
    desc_rdExp(rdExp1)





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
