#!/usr/bin/env python
# encoding: utf-8

from random import randint
import re

class RdExpression(object):
    """A generator of random expression builder"""

    def __init__(self, form, conditions = []):
        """Initiate the generator

        :param form: the form of the expression (/!\ variables need to be in brackets {})
        :param conditions: condition on variables (/!\ variables need to be in brackets {})

        """
        self._form = form
        self._conditions = conditions
        self._letters = self.get_letters()
        self._gene_varia = {}
        
    def get_letters(self):
        """Find letters in the form
        :returns: list of letters

        """
        pattern = "\{(\w+)\}"
        varia = re.findall(pattern, self._form)
        print(varia)
        return list(set(varia))

    def __call__(self, val_min = -10, val_max = 10):
        """RdExpression once it is initiate act like a function which create random expressions.

        :param val_min: minimum value random generation
        :param val_max: maximum value random generation
        :returns: an random expression

        """
        self.gene_varia(val_min, val_max)

        while not(self.val_conditions()):
            self.gene_varia(val_min, val_max)

        return self._form.format(**self._gene_varia)

    def gene_varia(self, val_min = -10, val_max = 10):
        """RAndomly generates variables/letters

        """
        for l in self._letters:
            self._gene_varia[l] = randint(val_min, val_max)

    def val_conditions(self):
        """Tells whether or not conditions are validates
        :returns: boolean

        """
        return eval(" and ".join(self._conditions).format(**self._gene_varia))


if __name__ == '__main__':
    form = "{a}x + 2*{b}"
    cond = ["{a} + {b} in [1, 2, 3, 4, 5]"]
    rdExp1 = RdExpression(form, cond)
    print(rdExp1())





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
