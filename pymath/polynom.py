#!/usr/bin/env python
# encoding: utf-8


from .expression import Expression
from .operator import op
from .generic import spe_zip, expand_list, isNumber, transpose_fill, flatten_list, isPolynom
from .render import txt
from .random_expression import RdExpression
from itertools import chain

__all__ = ["Polynom"]


class Polynom(object):

    """Docstring for Polynom. """

    @classmethod
    def random(self, coefs_form=[], conditions=[], letter = "x"):
        """ Create a random polynom from coefs_form and conditions 

        :param coefs_form: list of forms (one by coef) (ascending degree sorted)
        :param conditions: condition on variables 

        /!\ variables need to be in brackets {}

        """
        form = str(coefs_form)
        coefs = RdExpression(form, conditions)()
        coefs = [eval(i) if type(i)==str else i for i in eval(coefs)]
        return Polynom(coef = coefs, letter = letter)

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

    def __call__(self, value):
        """ Evaluate the polynom in value

        :returns: Expression ready to be simplify

        """
        if isNumber(value):
            postfix_exp = [value if i==self._letter else i for i in self.postfix]
        else:
            postfix_exp = [Expression(value) if i==self._letter else i for i in self.postfix]

        return Expression(postfix_exp)

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
        return str(Expression(self.postfix))

    def __repr__(self):
        return  "< Polynom " + str(self._coef) + ">"

    def coef_postfix(self, a, i):
        """Return the postfix display of a coeficient

        :param a: value for the coeficient (/!\ as a postfix list)
        :param i: power
        :returns: postfix tokens of coef

        >>> p = Polynom()
        >>> p.coef_postfix([3],2)
        [3, 'x', 2, '^', '*']
        >>> p.coef_postfix([0],1)
        []
        >>> p.coef_postfix([3],0)
        [3]
        >>> p.coef_postfix([3],1)
        [3, 'x', '*']
        >>> p.coef_postfix([1],1)
        ['x']
        >>> p.coef_postfix([1],2)
        ['x', 2, '^']

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
        # TODO: Faudrait factoriser un peu tout ça..! |dim. déc. 21 16:02:34 CET 2014
        postfix = []
        for (i,a) in list(enumerate(self._coef))[::-1]:
            operator = [op.add]
            operator_sub1 = []
            if type(a) == Expression:
                # case coef is an arithmetic expression
                c = self.coef_postfix(a.postfix_tokens,i)
                if c != []:
                    postfix.append(c)
                    if len(postfix) > 1:
                        postfix += operator

            elif type(a) == list:
                # case need to repeat the x^i
                for b in a:
                    if len(postfix) == 0 and isNumber(b) and b < 0:
                        try:
                            b = [(-b)[-1]]
                        except TypeError:
                            b = [-b]
                        operator_sub1 = [op.sub1]
                    elif len(postfix) > 0 and isNumber(b) and b < 0:
                        try:
                            b = [(-b)[-1]]
                        except TypeError:
                            b = [-b]
                        operator = [op.sub]
                    else:
                        b = [b]
                    c = self.coef_postfix(b,i)
                    if c != []:
                        postfix.append(c)
                        if len(postfix) > 1:
                            postfix += operator_sub1
                            postfix += operator
                        postfix += operator_sub1

            elif a != 0:
                if len(postfix) == 0 and a < 0:
                    try:
                        a = [(-a)[-1]]
                    except TypeError:
                        a = [-a]
                    operator_sub1 = [op.sub1]
                elif len(postfix) > 0 and a < 0:
                    try:
                        a = [(-a)[-1]]
                    except TypeError:
                        a = [-a]
                    operator = [op.sub]
                else:
                    a = [a]

                c = self.coef_postfix(a,i)
                if c != []:
                    postfix.append(c)
                    if len(postfix) > 1:
                        postfix += operator_sub1
                        postfix += operator
                    postfix += operator_sub1

        return flatten_list(postfix)

    def conv2poly(self, other):
        """Convert anything number into a polynom"""
        if isNumber(other) and not isPolynom(other):
            return Polynom([other])
        elif isPolynom(other):
            return other
        else:
            raise ValueError(type(other) + " can't be converted into a polynom")
    
    def reduce(self):
        """Compute coefficients which have same degree

        :returns: new Polynom with numbers coefficients
        """
        steps = []
        # gather steps for every coeficients
        coefs_steps = []
        for coef in self._coef:
            coef_steps = []
            if type(coef) == list:
                # On converti en postfix avec une addition
                postfix_add = self.postfix_add([i for i in coef if i!=0])
                # On converti en Expression
                coef_exp = Expression(postfix_add)

                old_render = Expression.get_render()
                Expression.set_render(lambda _,x:Expression(x))
                coef_steps = list(coef_exp.simplify())
                Expression.set_render(old_render)

            elif type(coef) == Expression:

                old_render = Expression.get_render()
                Expression.set_render(lambda _,x:Expression(x))
                coef_steps = list(coef.simplify())
                Expression.set_render(old_render)

            else:
                coef_steps = [coef]
                try:
                    coef_steps += coef.simplify()
                except AttributeError:
                    pass
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
        try:
            o_poly = self.conv2poly(other)
            return self._coef == o_poly._coef
        except TypeError:
            return 0

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

        #print("steps -> \n", "\n".join(["\t {}".format(s.postfix) for s in steps]))
        
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
    print(p, "+", q)
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

    print("\n Evaluer p ------")
    for i in p(3).simplify():
        print(i)

    print("\n Evaluer q ------")
    for i in q(3).simplify():
        print(i)
    

if __name__ == '__main__':
    #from .fraction import Fraction
    Expression.set_render(txt)
    p = Polynom([0, -2 ])
    q = Polynom([4, 0, 4])
    r = (p-q)[-1]
    print(r)

    #test(p,q)

    #print("\n")
    #p = Polynom([[1,0], [2,3,0]])
    #for i in p.simplify():
    #    print(i)

    #q = Polynom([0, Fraction(1,2), 0, Fraction(-4,3)])
    #test(p,q)

    #print("\n")
    #p = Polynom([-1,-2,-3])
    #print(p)

    #p = Polynom([-2])
    #q = Polynom([0,0,Fraction(1,2)])
    #test(p,q)

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

    #print("\n")
    #poly = Polynom.random(["[{a**2}, {a}]", "{2*a*b}", "{b**2}"]) 
    #for i in poly.simplify():
    #    print(i)

    import doctest
    doctest.testmod()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
