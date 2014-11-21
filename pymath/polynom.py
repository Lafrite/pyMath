#!/usr/bin/env python
# encoding: utf-8


from .expression import Expression
from .operator import op
from .generic import spe_zip, expand_list, isNumber, transpose_fill, flatten_list
#from .generic import spe_zip, sum_postfix, expand_list, isNumber
from .render import txt
from itertools import chain

__all__ = ["Polynom"]


class Polynom(object):

    """Docstring for Polynom. """

    def __init__(self, coef = [1], letter = "x" ):
        """Initiate the polynom

        :param coef: coefficients of the polynom (ascending degree sorted)
            3 possibles type of coefficent:
                - a : simple "number". [1,2] designate 1 + 2x
                - [a,b,c]: list of coeficient for same degree. [1,[2,3],4] designate 1 + 2x + 3x + 4x^2
                - a: a Expression. [1, Expression("2+3"), 4] designate 1 + (2+3)x + 4x^2
        :param letter: the string describing the unknown

        >>> Polynom([1,2,3]).mainOp
        '+'
        >>> Polynom([1]).mainOp
        '*'
        >>> Polynom([1,2, 3])._letter
        'x'
        >>> Polynom([1, 2, 3], "y")._letter
        'y'
        """
        self.feed_coef(coef)
        self._letter = letter

        
        if self.is_monom():
            self.mainOp = "*"
        else:
            self.mainOp = "+"

        self._isPolynom = 1

    def feed_coef(self, l_coef):
        """Feed coef of the polynom. Manage differently whether it's a number or an expression
        
        :l_coef: list of coef
        """
        self._coef = []
        for coef in l_coef:
            if type(coef) == list and len(coef)==1:
                self._coef.append(coef[0])
            else:
                self._coef.append(coef)

    def get_degree(self):
        """Getting the degree fo the polynom

        :returns: the degree of the polynom

        >>> Polynom([1, 2, 3]).get_degree()
        2
        >>> Polynom([1]).get_degree()
        0
        """
        return len(self._coef) - 1

    def is_monom(self):
        """is the polynom a monom (only one coefficent)

        :returns: 1 if yes 0 otherwise

        >>> Polynom([1, 2, 3]).is_monom()
        0
        >>> Polynom([1]).is_monom()
        1
        """
        if len([i for i in self._coef if i != 0])==1:
            return 1
        else:
            return 0

    def __str__(self):
        return txt(self.postfix)

    def __repr__(self):
        return  "< Polynom " + str(self._coef) + ">"

    def coef_postfix(self, a, i):
        """Return the postfix display of a coeficient

        :param a: value for the coeficient (/!\ as a postfix list)
        :param i: power
        :returns: postfix tokens of coef

        """
        # TODO: Couille certaine avec txt à qui il fait donner des opérateurs tout beau! |mar. nov. 11 13:08:35 CET 2014
        ans =[] 
        if a == [0]:
            pass
        elif i == 0:
            ans = a
        elif i == 1:
            ans = a * (a!=[1]) + [self._letter] + [op.mul] *  (a!=[1]) 
        else:
            ans = a * (a!=[1]) + [self._letter, i, op.pw] + [op.mul] *  (a!=[1]) 
        
        return ans

    @property
    def postfix(self):
        """Return the postfix form of the polynom

        :returns: the postfix list of polynom's tokens

        """
        postfix = []
        for (i,a) in list(enumerate(self._coef))[::-1]:
            if type(a) == Expression:
                # case coef is an arithmetic expression
                c = self.coef_postfix(a.postfix_tokens,i)
                if c != []:
                    postfix.append(c)

            elif type(a) == list:
                # case need to repeat the x^i
                for b in a:
                    c = self.coef_postfix([b],i)
                    if c != []:
                        postfix.append(c)

            elif a != 0:
                c = self.coef_postfix([a],i)
                if c != []:
                    postfix.append(c)

        return flatten_list(self.postfix_add(postfix))

    def conv2poly(self, other):
        """Convert anything number into a polynom"""
        if isNumber(other) and not self.isPolynom(other):
            return Polynom([other])
        elif self.isPolynom(other):
            return other
        else:
            raise ValueError(type(other) + " can't be converted into a polynom")

    def isPolynom(self, other):
        try:
            other._isPolynom
        except AttributeError:
                return 0
        return  1
    
    def reduce(self):
        """Compute coefficients which have same degree

        :returns: new Polynom with numbers coefficients
        """
        steps = []
        # gather steps for every coeficients
        coefs_steps = []
        for coef in self._coef:
            coef_steps = []
            if type(coef) != Expression:
                # On converti en postfix avec une addition
                postfix_add = self.postfix_add(coef)
                # On converti en Expression
                coef_exp = Expression(postfix_add)
            else:
                coef_exp = coef

            # On fait réduire l'expression puis on ajoute dans steps
            Expression.set_render(lambda _,x:Expression(x))
            coef_steps = list(coef_exp.simplify())
            Expression.set_df_render()

            # On ajoute toutes ces étapes
            coefs_steps.append(coef_steps)

        # On retourne la matrice
        ans = []
        for coefs in transpose_fill(coefs_steps):
            ans.append(Polynom(coefs, self._letter))
            
        return ans

    @staticmethod
    def postfix_add(numbers):
        """Convert a list of numbers into a postfix addition
        
        :numbers: list of numbers
        :returns: Postfix list of succecive attition of number

        >>> Polynom.postfix_add([1])
        [1]
        >>> Polynom.postfix_add([1, 2])
        [1, 2, '+']
        >>> Polynom.postfix_add([1, 2, 3])
        [1, 2, '+', 3, '+']
        >>> Polynom.postfix_add(1)
        [1]
        """
        if not type(numbers) == list:
            return [numbers]
        else:
            ans = [[a, op.add] if i!=0 else [a] for (i,a) in enumerate(numbers)]
            return list(chain.from_iterable(ans))
            
    def simplify(self):
        """Same as reduce """
        return self.reduce()

    def __eq__(self, other):
        o_poly = self.conv2poly(other)
        return self._coef == o_poly._coef

    def __add__(self, other):
        steps = []

        o_poly = self.conv2poly(other)

        n_coef = spe_zip(self._coef, o_poly._coef)
        p = Polynom(n_coef)
        steps.append(p)

        steps += p.simplify()
        return steps

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return Polynom([-i for i in self._coef], letter = self._letter)

    def __sub__(self, other):
        o_poly = self.conv2poly(other)
        o_poly = -o_poly

        return self.__add__(o_poly)

    def __rsub__(self, other):
        o_poly = self.conv2poly(other)
        
        return o_poly.__sub__(-self)
    
    def __mul__(self, other):
        steps = []
        o_poly = self.conv2poly(other)

        coefs = []
        for (i,a) in enumerate(self._coef):
            for (j,b) in enumerate(o_poly._coef):
                if a == 0 or b == 0:
                    elem = 0
                else:
                    elem = Expression([a, b, op.mul])
                try:
                    if coefs[i+j]==0:
                        coefs[i+j] = elem
                    elif elem != 0:
                        coefs[i+j] = [coefs[i+j], elem]
                except IndexError:
                    coefs.append(elem)

        p = Polynom(coefs)
        steps.append(p)
        
        steps += p.simplify()
        
        return steps

    def __rmul__(self, other):
        o_poly = self.conv2poly(other)

        return o_poly.__mul__(self)


def test(p,q):
    print("---------------------")
    print("---------------------")
    print("p : ",p)
    print("q : ",q)

    print("\n Plus ------")
    for i in (p + q):
        #print(repr(i))
        #print("\t", str(i.postfix))
        print(i)

    print("\n Moins ------")
    for i in (p - q):
        #print(repr(i))
        #print("\t", str(i.postfix))
        print(i)

    print("\n Multiplier ------")
    for i in (p * q):
        #print(repr(i))
        #print("\t", str(i.postfix))
        print(i)
    

if __name__ == '__main__':
    from .fraction import Fraction
    p = Polynom([1, -2 ])
    q = Polynom([4, 7])
    test(p,q)

    q = Polynom([0, Fraction(1,2), 0, Fraction(-4,3)])
    test(p,q)

    #p = Polynom([1, 1, 1 ])
    #print(p)


    #print("-- Poly étrange --")
    #p = Polynom([1, [2, 3], 4], "x")
    #print(repr(p))
    #for i in p.simplify():
    #    print(i)
    #print("-- Poly étrange --")
    #p = Polynom([1, [[2, 3, "*"], [4,5,"*"]], 4], "x")
    #print(repr(p))
    #print(p)
    #for i in p.simplify():
    #    print(repr(i))

    import doctest
    doctest.testmod()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
