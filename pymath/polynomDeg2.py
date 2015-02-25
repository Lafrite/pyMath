#!/usr/bin/env python
# encoding: utf-8

from .polynom import Polynom
from .expression import Expression
from .operator import op
from math import sqrt


class Polynom_deg2(Polynom):

    """ Degree 2 polynoms
    Child of Polynom with some extra tools
    """

    def __init__(self, coefs = [0, 0, 1], letter = "x"):
        """@todo: to be defined1. """
        if len(coefs) < 3 or len(coefs) > 4:
            raise ValueError("Polynom_deg2 have to be degree 2 polynoms, they need 3 coefficients, {} are given".format(len(coefs)))
        if coefs[2] == 0:
            raise ValueError("Polynom_deg2 have to be degree 2 polynoms, coefficient of x^2 can't be 0")
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

        >>> P = Polynom_deg2([1,2,3])
        >>> P.delta
        < Expression [2, 2, '^', 4, 3, 1, '*', '*', '-']>
        >>> for i in P.delta.simplify():
            print(i)
        2^{  2 } - 4 \times 3 \times 1
        4 - 4 \times 3
        4 - 12
        -8
        >>> P.delta.simplified()
        -8
        """

        return Expression([self.b, 2, op.pw, 4, self.a, self.c, op.mul, op.mul, op.sub])

    def roots(self):
        """ Compute roots of the polynom

        /!\ Can't manage exact solution because of pymath does not handle sqare root yet

        # TODO: Pymath has to know how to compute with sqare root |mar. févr. 24 18:40:04 CET 2015

        >>> P = Polynom_deg2([1, 1, 1])
        >>> P.roots()
        []
        >>> P = Polynom_deg2([1, 2, 1])
        >>> P.roots()
        [-1.0]
        >>> P = Polynom_deg2([-1, 0, 1])
        >>> P.roots()
        [-1.0, 1.0]
        """
        if self.delta.simplified() > 0:
            self.roots = [(-self.b - sqrt(self.delta.simplified()))/(2*self.a), (-self.b + sqrt(self.delta.simplified()))/(2*self.a)]
        elif self.delta.simplified() == 0:
            self.roots = [-self.b /(2*self.a)]
        else:
            self.roots = []
        return self.roots

    def tbl_sgn(self):
        """ Return the sign line for tkzTabLine

        >>> P = Polynom_deg2([2, 5, 2])
        >>> P.tbl_sgn()
        '\\tkzTabLine{, +, z, -, z , +,}'
        >>> P = Polynom_deg2([2, 1, -2])
        >>> P.tbl_sgn()
        '\\tkzTabLine{, -, z, +, z , -,}'
        >>> P = Polynom_deg2([1, 2, 1])
        >>> P.tbl_sgn()
        '\\tkzTabLine{, +, z, +,}'
        >>> P = Polynom_deg2([0, 0, -2])
        >>> P.tbl_sgn()
        '\\tkzTabLine{, -, z, -,}'
        >>> P = Polynom_deg2([1, 0, 1])
        >>> P.tbl_sgn()
        '\\tkzTabLine{, +,}'
        >>> P = Polynom_deg2([-1, 0, -1])
        >>> P.tbl_sgn()
        '\\tkzTabLine{, -,}'
        """
        if self.delta.simplified() > 0:
            if self.a > 0:
                return "\\tkzTabLine{, +, z, -, z , +,}"
            else:
                return "\\tkzTabLine{, -, z, +, z , -,}"
        elif self.delta.simplified() == 0:
            if self.a > 0:
                return "\\tkzTabLine{, +, z, +,}"
            else:
                return "\\tkzTabLine{, -, z, -,}"
        else:
            if self.a > 0:
                return "\\tkzTabLine{, +,}"
            else:
                return "\\tkzTabLine{, -,}"

    




if __name__ == '__main__':
   # from .render import txt
   # with Expression.tmp_render(txt):
   #     P = Polynom_deg2([2, 3, 4])
   #     print(P)

   #     print("Delta")
   #     for i in P.delta.simplify():
   #         print(i)

    import doctest
    doctest.testmod()
        



# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
