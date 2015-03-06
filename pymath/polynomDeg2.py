#!/usr/bin/env python
# encoding: utf-8

from .polynom import Polynom
from .expression import Expression
from .operator import op
from .random_expression import RdExpression
from math import sqrt

__all__ = ["Polynom_deg2"]

class Polynom_deg2(Polynom):

    """ Degree 2 polynoms
    Child of Polynom with some extra tools
    """

    @classmethod
    def random(self, coefs_form = ["{c}", "{b}", "{a}"], conditions = [], letter = "x"):
        """ Create a 2nd degree poly from coefs_form ans conditions

        :param coefs_form: list of forms (one by coef) (ascending degree sorted)
        :param conditions: condition on variables 
        :param letter: the letter for the polynom

        """
        if len(coefs_form) != 3:
            raise ValueError("Polynom_deg2 have to be degree 2 polynoms, they need 3 coefficients, {} are given".format(len(coefs_form)))

        form = str(coefs_form)
        # On créé les valeurs toutes concaténées dans un string
        coefs = RdExpression(form, conditions)()
        # On "parse" ce string pour créer les coefs
        coefs = [eval(i) if type(i)==str else i for i in eval(coefs)]
        # Création du polynom
        return Polynom_deg2(coefs = coefs, letter = letter)

    def __init__(self, coefs = [0, 0, 1], letter = "x"):
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
        -8
        >>> for i in P.delta.explain():
        ...     print(i)
        2^{  2 } - 4 \\times 3 \\times 1
        4 - 4 \\times 3
        4 - 12
        -8
        """

        return Expression([self.b, 2, op.pw, 4, self.a, self.c, op.mul, op.mul, op.sub]).simplify()

    @property
    def alpha(self):
        """ Compute alpha the abcisse of the extremum
        
        >>> P = Polynom_deg2([1,2,3])
        >>> P.alpha
        < Fraction -1 / 3>
        >>> for i in P.alpha.explain():
        ...     print(i)
        \\frac{ - 2 }{ 2 \\times 3 }
        \\frac{ -2 }{ 6 }
        \\frac{ ( -1 ) \\times 2 }{ 3 \\times 2 }
        \\frac{ -1 }{ 3 }
        """
        return Expression([self.b, op.sub1, 2, self.a, op.mul, op.div]).simplify()

    @property
    def beta(self):
        """ Compute beta the extremum of self

        >>> P = Polynom_deg2([1,2,3])
        >>> P.beta
        < Fraction 2 / 3>
        >>> for i in P.beta.explain(): # Ça serait bien que l'on puisse enlever des étapes maintenant...
        ...     print(i)
        3 \\times \\frac{ -1 }{ 3 }^{  2 } + 2 \\times \\frac{ -1 }{ 3 } + 1
        3 \\times \\frac{ 1 }{ 9 } + \\frac{ -2 }{ 3 } + 1
        \\frac{ 1 }{ 3 } + \\frac{ -2 }{ 3 } + 1
        \\frac{ -1 }{ 3 } + 1
        \\frac{ 2 }{ 3 }
        """
        return self(self.alpha).simplify()

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
        if self.delta > 0:
            self.roots = [(-self.b - sqrt(self.delta))/(2*self.a), (-self.b + sqrt(self.delta))/(2*self.a)]
        elif self.delta == 0:
            self.roots = [-self.b /(2*self.a)]
        else:
            self.roots = []
        return self.roots

    def tbl_sgn(self):
        """ Return the sign line for tkzTabLine

        >>> P = Polynom_deg2([2, 5, 2])
        >>> print(P.tbl_sgn())
        \\tkzTabLine{, +, z, -, z , +,}
        >>> P = Polynom_deg2([2, 1, -2])
        >>> print(P.tbl_sgn())
        \\tkzTabLine{, -, z, +, z , -,}
        >>> P = Polynom_deg2([1, 2, 1])
        >>> print(P.tbl_sgn())
        \\tkzTabLine{, +, z, +,}
        >>> P = Polynom_deg2([0, 0, -2])
        >>> print(P.tbl_sgn())
        \\tkzTabLine{, -, z, -,}
        >>> P = Polynom_deg2([1, 0, 1])
        >>> print(P.tbl_sgn())
        \\tkzTabLine{, +,}
        >>> P = Polynom_deg2([-1, 0, -1])
        >>> print(P.tbl_sgn())
        \\tkzTabLine{, -,}
        """
        if self.delta > 0:
            if self.a > 0:
                return "\\tkzTabLine{, +, z, -, z , +,}"
            else:
                return "\\tkzTabLine{, -, z, +, z , -,}"
        elif self.delta == 0:
            if self.a > 0:
                return "\\tkzTabLine{, +, z, +,}"
            else:
                return "\\tkzTabLine{, -, z, -,}"
        else:
            if self.a > 0:
                return "\\tkzTabLine{, +,}"
            else:
                return "\\tkzTabLine{, -,}"

    def tbl_variation(self, limits = False):
        """Return the variation line for tkzTabVar

        :param limit: Display or not limits in tabular

        >>> P = Polynom_deg2([1,2,3])
        >>> print(P.tbl_variation())
        \\tkzTabVar{+/{}, -/{$\\frac{ 2 }{ 3 }$}, +/{}}
        >>> print(P.tbl_variation(limits = True))
        \\tkzTabVar{+/{$+\\infty$}, -/{$\\frac{ 2 }{ 3 }$}, +/{$+\\infty$}}

        """
        beta = self.beta
        if limits:
            if self.a > 0:
                return "\\tkzTabVar{+/{$+\\infty$}, -/{$" + str(beta) + "$}, +/{$+\\infty$}}"
            else:
                return "\\tkzTabVar{-/{$-\\infty$}, +/{$" + str(beta) + "$}, -/{$-\\infty$}}"
        else:
            if self.a > 0:
                return "\\tkzTabVar{+/{}, -/{$" + str(beta) + "$}, +/{}}"
            else:
                return "\\tkzTabVar{-/{}, +/{$" + str(beta) + "$}, -/{}}"


    



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
