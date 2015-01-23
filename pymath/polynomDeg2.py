#!/usr/bin/env python
# encoding: utf-8

from .polynom import Polynom
from .expression import Expression
from .operator import op
from math import sqrt


class Polynom_deg2(Polynom):

    """ Degree 2 polynoms
    Child of Polynom with some extro tools
    """

    def __init__(self, coefs = [0, 0, 1], letter = "x"):
        """@todo: to be defined1. """
        Polynom.__init__(self, coefs, letter)

    @property
    def a(self):
        return self._coef[2]

    @property
    def b(self):
        return self._coef[1]

    @property
    def c(self):
        return self._coef[0]

    @property
    def delta(self):
        """Compute the discriminant expression
        :returns: discriminant expression

        """
        return Expression([self.b, 2, op.pw, 4, self.a, self.c, op.mul, op.mul, op.sub])

    def roots(self):
        """Compute roots of the polynom
        """
        if self.delta > 0:
            roots = [(-self.b - sqrt(self.delta)




if __name__ == '__main__':
    from .render import txt
    with Expression.tmp_render(txt):
        P = Polynom_deg2([2, 3, 4])
        print(P)

        print("Delta")
        for i in P.delta.simplify():
            print(i)
        



# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
