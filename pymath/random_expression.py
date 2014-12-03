#!/usr/bin/env python
# encoding: utf-8

from random import randint
from .expression import Expression
from .render import tex, txt
import re
import pyparsing
from .generic import flatten_list

from .arithmetic import gcd

class RdExpression(object):
    """
    A generator of random expression builder

    Two forms are available:
        - exp: return the expression through Expression class (default)
        - raw: return the expression as a raw string
    This can be set globally with

        RdExpression.FORM

    or temporary with 
        - "raw_exp" or "raw_str" methods 
    
    """

    FORM = "exp"
    DEFAULT_FORM = "exp"

    @classmethod
    def set_form(cls, form):
        """ Define whether RdExpression create expression with Expression (nice render) or if it only replace inside {} not taking care or render

        >>> form = "{a}*{b}"
        >>> exp = RdExpression(form)()
        >>> print(type(exp))
        <class 'pymath.expression.Expression'>
        >>> RdExpression.set_form("raw")
        >>> form = "{a}*{b}"
        >>> exp = RdExpression(form)()
        >>> print(type(exp))
        <class 'str'>
        """

        cls.FORM = form

    @classmethod
    def set_df_form(cls):
        cls.set_form(cls.DEFAULT_FORM)

    def __init__(self, form, conditions = []):
        """Initiate the generator

        :param form: the form of the expression (/!\ variables need to be in brackets {})
        :param conditions: condition on variables (/!\ variables need to be in brackets {})

        """
        self._form = form
        self._conditions = conditions

        self._letters = self.get_letters()
        self._gene_varia = {}
        self._gene_2replaced= {}

    def get_2replaced(self):
        """Get elements of self._form which will have to be replaced
        :returns: set for elements which have to be replaced

        """
        #pattern = "\{(.*?)\}" #select inside {} non greedy way
        #varia_form = re.findall(pattern, self._form)

        # TODO: Bug with varia with spaces |dim. nov. 23 10:44:34 CET 2014
        varia_form = flatten_list([eval(str(i[0])) for i in pyparsing.nestedExpr('{','}').searchString(self._form)])
        varia_form = set(varia_form)

        varia_cond = set()
        for c in self._conditions:
            c_varia_cond = flatten_list([eval(str(i[0])) for i in pyparsing.nestedExpr('{','}').searchString(c)])
            varia_cond = varia_cond | set(c_varia_cond)
        
        self._2replaced = varia_cond | varia_form

        return self._2replaced
        
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


    def __call__(self, val_min = -10, val_max = 10):
        """RdExpression once it is initiate act like a function which create random expressions.

        :param val_min: minimum value random generation
        :param val_max: maximum value random generation
        :param render: Render of the expression (returns an Expression by default)
        :returns: an formated random expression 

        """
        if self.FORM == "exp":
            return self.raw_exp(val_min, val_max)
        elif self.FORM == "raw":
            return self.raw_str(val_min, val_max)
        else:
            raise ValueError(self.FORM , " is an undefined form for self.FORM")

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
        """Randomly generates variables/letters

        Varia can't be equal to 0

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
            return eval(" and ".join(self._conditions).format(**self._gene_2replaced))
        else:
            return True

def desc_rdExp(rdExp):
    print("--------------------")
    print("form: ",rdExp._form)
    print("Conditions: ",rdExp._conditions)
    print("Letters: ", rdExp._letters)
    print("2replaced: ", rdExp._2replaced)
    print("Call : ", rdExp())
    print("type: ",type(rdExp()))
    print("Gene varia: ", rdExp._gene_varia)
    print("Gene 2replaced: ", rdExp._gene_2replaced)
    print('')


if __name__ == '__main__':
    # Adapt render to consol display
    #Expression.set_render(txt)

    RdExpression.set_form("raw")
    form = "{a}*-14 / (2*{b}) / -23 / 4"
    cond = ["{a} + {b} in [1, 2, 3, 4, 5]", "{a} not in [1]", "{b} not in [1]"]
    rdExp1 = RdExpression(form, cond)
    desc_rdExp(rdExp1)
    rdExp2 = RdExpression(form)
    desc_rdExp(rdExp2)

    RdExpression.set_df_form()
    form = "{a+a*10}*4 + {a} + 2*{b}"
    cond = ["{a} + {b} in [1, 2, 3, 4, 5]", "abs({a}) not in [1]", "{b} not in [1]", "gcd({a},{b}) == 1"]
    rdExp3 = RdExpression(form, cond)
    desc_rdExp(rdExp3)

    form = "{a+a*10}*4 + {a} + 2*{b}"
    cond = ["{a-b} + {b} in list(range(20))", "abs({a}) not in [1]", "{b} not in [1]", "gcd({a},{b}) == 1"]
    rdExp3 = RdExpression(form, cond)
    desc_rdExp(rdExp3)

    import doctest
    doctest.testmod()



# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
