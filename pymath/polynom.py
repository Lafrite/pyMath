#!/usr/bin/env python
# encoding: utf-8


from .expression import Expression
from .operator import op
from .generic import isNumerand
from .random_expression import RdExpression
from .abstract_polynom import AbstractPolynom

from functools import wraps
import inspect

__all__ = ["Polynom"]

def polynom_factory(func):
    """ Decorator which specify the type of polynom that the function returns """
    @wraps(func)
    def wrapper(*args, **kwrds):
        P = func(*args, **kwrds)
        if isinstance(P,Polynom) and P.degree == 2:
            from .polynomDeg2 import Polynom_deg2
            new_P = Polynom_deg2(poly=P)
            new_P.steps = P.steps
            return new_P
        else:
            return P
    return wrapper

class Polynom(AbstractPolynom):

    """Polynom view as a function.
    
    It can be initiate like a AbstractPolynom
    # Put example
    Randomly
    # Put example
    It can be evaluate
    # Put example
    And derivate
    # Put example

    """

    @classmethod
    def random(self, coefs_form=[], conditions=[], letter = "x", degree = 0, name = "P"):
        """ Create a random polynom from coefs_form and conditions 

        :param coefs_form: list of forms (one by coef) (ascending degree sorted)
        :param conditions: condition on variables 
        :param letter: the letter for the polynom
        :param degree: degree of the polynom (can't be used with coefs_form, it will be overwrite) - can't be higher than 26 (number of letters in alphabet)

        /!\ variables need to be in brackets {}

        >>> Polynom.random(["{b}", "{a}"]) # doctest:+ELLIPSIS
        < Polynom ...
        >>> Polynom.random(degree = 2) # doctest:+ELLIPSIS
        < Polynom ...
        >>> Polynom.random(degree = 2, conditions=["{b**2-4*a*c}>0"]) # Polynom deg 2 with positive Delta (ax^2 + bx + c)
        < Polynom ...
        >>> Polynom.random(["{c}", "{b}", "{a}"], conditions=["{b**2-4*a*c}>0"]) # Same as above
        < Polynom ...

        """
        if (degree > 0 and degree < 26):
            # Générer assez de lettre pour les coefs
            coefs_name = map(chr, range(97, 98+degree))
            coefs_form = ["{" + i + "}" for i in coefs_name][::-1]

        form = str(coefs_form)
        # On créé les valeurs toutes concaténées dans un string
        coefs = RdExpression(form, conditions)()
        # On "parse" ce string pour créer les coefs
        coefs = [eval(i) if type(i)==str else i for i in eval(coefs)]
        # Création du polynom
        return Polynom(coefs = coefs, letter = letter, name = name)

    def __init__(self, coefs = [1], letter = "x", name = "P"):
        """Initiate the polynom

        :param coef: coefficients of the polynom (ascending degree sorted)
            3 possibles type of coefficent:
                - a : simple "number". [1,2] designate 1 + 2x
                - [a,b,c]: list of coeficient for same degree. [1,[2,3],4] designate 1 + 2x + 3x + 4x^2
                - a: a Expression. [1, Expression("2+3"), 4] designate 1 + (2+3)x + 4x^2
        :param letter: the string describing the unknown
        :param name: Name of the polynom

        >>> P = Polynom([1, 2, 3])
        >>> P.mainOp
        '+'
        >>> P.name
        'P'
        >>> P._letter
        'x'
        >>> Polynom([1]).mainOp
        '*'
        >>> Polynom([0, 0, 3]).mainOp
        '*'
        >>> Polynom([1, 2, 3])._letter
        'x'
        >>> Polynom([1, 2, 3], "y")._letter
        'y'
        >>> Polynom([1, 2, 3], name = "Q").name
        'Q'
        """
        super(Polynom, self).__init__(coefs, letter, name)

    def __call__(self, value):
        """ Evaluate the polynom in value

        :returns: Expression ready to be simplify

        >>> P = Polynom([1, 2, 3])
        >>> P(2)
        17
        >>> for i in P(2).explain():
        ...     print(i)
        3 \\times 2^{  2 } + 2 \\times 2 + 1
        3 \\times 4 + 4 + 1
        12 + 4 + 1
        16 + 1
        17
        >>> Q = P("1+h")
        >>> print(Q)
        3 h^{  2 } + 8 h + 6
        >>> R = P(Q)
        """
        if isNumerand(value) or Expression.isExpression(value):
            postfix_exp = [value if i==self._letter else i for i in self.postfix_tokens]
        else:
            postfix_exp = [Expression(value) if i==self._letter else i for i in self.postfix_tokens]

        return Expression(postfix_exp).simplify()

    def derivate(self):
        """ Return the derivated polynom 
        
        >>> P = Polynom([1, 2, 3])
        >>> Q = P.derivate()
        >>> Q
        < Polynom [2, 6]>
        >>> print(Q.name)
        P'
        >>> for i in Q.explain():
        ...     print(i)
        2 \\times 3 x + 1 \\times 2
        6 x + 2
        """
        derv_coefs = []
        for (i,c) in enumerate(self._coef):
            derv_coefs += [Expression([i, c, op.mul])]

        ans = Polynom(derv_coefs[1:]).simplify()
        ans.name = self.name + "'"
        return ans

# Decorate methods which may return Polynoms
methods_list = ["__add__", "__call__", "__mul__", "__neg__", "__pow__",
        "__radd__", "__rmul__", "__rsub__", "__sub__", "derivate", 
        "reduce", "simplify", "random"]
for name, func in inspect.getmembers(Polynom):
    if name in methods_list:
        setattr(Polynom, name, polynom_factory(func))


def test(p,q):
    print("---------------------")
    print("---------------------")
    print("p : ",p)
    print("q : ",q)

    print("\n Plus ------")
    print(p, "+", q)
    for i in (p + q):
        #print(repr(i))
        #print("\t", str(i.postfix_tokens))
        print(i)

    print("\n Moins ------")
    for i in (p - q):
        #print(repr(i))
        #print("\t", str(i.postfix_tokens))
        print(i)

    print("\n Multiplier ------")
    for i in (p * q):
        #print(repr(i))
        #print("\t", str(i.postfix_tokens))
        print(i)

    print("\n Evaluer p ------")
    for i in p(3).simplify():
        print(i)

    print("\n Evaluer q ------")
    for i in q(3).simplify():
        print(i)
    

if __name__ == '__main__':
    #from .fraction import Fraction
    #with Expression.tmp_render(txt):
    #    p = Polynom([1, 2, 3])
    #    q = Polynom([4, 5, 6])
    #    for i in (p*q).explain():
    #        print(i)
    #     r = Polynom([0,1])
    #     for i in (r*3).explain():
    #         print(i)
    #     print("q = ", q)
    #     r = q.reduce()
    #     print("r = ", r)
    #     for i in r.explain():
    #         print("q = ", i)
    #    print(p-q)
    #    for i in p-q:
    #        print(i)
    #Polynom.random(degree = 2, conditions=["{b**2-4*a*c}>0"]) # Polynom deg 2 with positive Delta (ax^2 + bx + c)

    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
