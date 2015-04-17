#!/usr/bin/env python
# encoding: utf-8

from .explicable import Explicable
from .expression import Expression
from .operator import op
from .generic import spe_zip, expand_list, isNumber, transpose_fill, flatten_list, isPolynom, isNumerand
from .render import txt,tex
from itertools import chain
from functools import wraps

def power_cache(fun):
    """Decorator which cache calculated powers of polynoms """
    cache  = {}
    @wraps(fun)
    def cached_fun(self, power):
        #print("cache -> ", cache)
        if (tuple(self._coef), power) in cache.keys():
            return cache[(tuple(self._coef), power)]
        else:
            poly_powered = fun(self, power)
            cache[(tuple(self._coef), power)] = poly_powered
            return poly_powered
    return cached_fun

class AbstractPolynom(Explicable):

    """The mathematic definition of a polynom. It will be the parent class of Polynom (classical polynoms) and later of SquareRoot polynoms"""

    def __init__(self, coefs = [1], letter = "x", name = "P"):
        """Initiate the polynom

        :param coef: coefficients of the polynom (ascending degree sorted)
            3 possibles type of coefficent:
                - a : simple "number". [1,2] designate 1 + 2x
                - [a,b,c]: list of coeficient for same degree. [1,[2,3],4] designate 1 + 2x + 3x + 4x^2
                - a: a Expression. [1, Expression("2+3"), 4] designate 1 + (2+3)x + 4x^2
        :param letter: the string describing the unknown
        :param name: Name of the polynom

        >>> P = AbstractPolynom([1, 2, 3])
        >>> P.mainOp
        '+'
        >>> P.name
        'P'
        >>> P._letter
        'x'
        >>> AbstractPolynom([1]).mainOp
        '*'
        >>> AbstractPolynom([0, 0, 3]).mainOp
        '*'
        >>> AbstractPolynom([1, 2, 3])._letter
        'x'
        >>> AbstractPolynom([1, 2, 3], "y")._letter
        'y'
        >>> AbstractPolynom([1, 2, 3], name = "Q").name
        'Q'
        """
        super(AbstractPolynom, self).__init__()

        try:
            # Remove 0 at the end of the coefs
            while coefs[-1] == 0:
                coefs = coefs[:-1]
        except IndexError:
            pass

        if coefs == []:
            coefs = [0]

        self.feed_coef(coefs)
        self._letter = letter
        self.name = name
        
        if self.is_monom():
            self.mainOp = op.mul
        else:
            self.mainOp = op.add

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

    @property
    def degree(self):
        """Getting the degree fo the polynom

        :returns: the degree of the polynom

        >>> AbstractPolynom([1, 2, 3]).degree
        2
        >>> AbstractPolynom([1]).degree
        0
        """
        return len(self._coef) - 1

    def is_monom(self):
        """is the polynom a monom (only one coefficent)

        :returns: 1 if yes 0 otherwise

        >>> AbstractPolynom([1, 2, 3]).is_monom()
        0
        >>> AbstractPolynom([1]).is_monom()
        1
        """
        if len([i for i in self._coef if i != 0])==1:
            return 1
        else:
            return 0

    def give_name(self, name):
        self.name = name

    def __str__(self):
        return str(Expression(self.postfix_tokens))

    def __repr__(self):
        return  "< " + str(self.__class__) + " " + str(self._coef) + ">"

    def __txt__(self):
        return txt(self.postfix_tokens)

    def __tex__(self):
        return tex(self.postfix_tokens)

    def coef_postfix(self, a, i):
        """Return the postfix display of a coeficient

        :param a: value for the coeficient (/!\ as a postfix list)
        :param i: power
        :returns: postfix tokens of coef

        >>> p = AbstractPolynom()
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
    def postfix_tokens(self):
        """Return the postfix form of the polynom

        :returns: the postfix list of polynom's tokens

        >>> p = AbstractPolynom([1, 2])
        >>> p.postfix_tokens
        [2, 'x', '*', 1, '+']
        >>> p = AbstractPolynom([1, -2])
        >>> p.postfix_tokens
        [2, 'x', '*', '-', 1, '+']
        >>> p = AbstractPolynom([1,2,3])
        >>> p.postfix_tokens
        [3, 'x', 2, '^', '*', 2, 'x', '*', '+', 1, '+']
        >>> p = AbstractPolynom([1])
        >>> p.postfix_tokens
        [1]
        >>> p = AbstractPolynom([0])
        >>> p.postfix_tokens
        [0]
        >>> p = AbstractPolynom([1,[2,3]])
        >>> p.postfix_tokens
        [2, 'x', '*', 3, 'x', '*', '+', 1, '+']
        >>> p = AbstractPolynom([1,[2,-3]])
        >>> p.postfix_tokens
        [2, 'x', '*', 3, 'x', '*', '-', 1, '+']
        >>> p = AbstractPolynom([1,[-2,-3]])
        >>> p.postfix_tokens
        [2, 'x', '*', '-', 3, 'x', '*', '-', 1, '+']
        >>> from pymath.expression import Expression
        >>> from pymath.operator import op
        >>> e = Expression([2,3,op.add])
        >>> p = AbstractPolynom([1,e])
        >>> p.postfix_tokens
        [2, 3, '+', 'x', '*', 1, '+']

        """
        if self == 0:
            return [0]
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
                    operator = [op.add]
                    operator_sub1 = []
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
        """Convert anything number into a polynom
        
        >>> P = AbstractPolynom([1,2,3])
        >>> P.conv2poly(1)
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [1]>
        >>> P.conv2poly(0)
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [0]>
        
        """
        if isNumber(other) and not isPolynom(other):
            return AbstractPolynom([other], letter = self._letter)
        elif isPolynom(other):
            return other
        else:
            raise ValueError(type(other) + " can't be converted into a polynom")
    
    def reduce(self):
        """Compute coefficients which have same degree

        :returns: new AbstractPolynom with numbers coefficients

        >>> P = AbstractPolynom([1,2,3])
        >>> Q = P.reduce()
        >>> Q
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [1, 2, 3]>
        >>> Q.steps
        []
        >>> P = AbstractPolynom([[1,2], [3,4,5], 6])
        >>> Q = P.reduce()
        >>> Q
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [3, 12, 6]>
        >>> Q.steps
        [< <class 'pymath.abstract_polynom.AbstractPolynom'> [< <class 'pymath.expression.Expression'> [1, 2, '+'] >, < <class 'pymath.expression.Expression'> [3, 4, '+', 5, '+'] >, 6]>, < <class 'pymath.abstract_polynom.AbstractPolynom'> [3, < <class 'pymath.expression.Expression'> [7, 5, '+'] >, 6]>]
        """
    
        # TODO: It doesn't not compute quick enough |ven. févr. 27 18:04:01 CET 2015

        # gather steps for every coeficients
        coefs_steps = []
        for coef in self._coef:
            coef_steps = []
            if type(coef) == list:
                # On converti en postfix avec une addition
                postfix_add = self.postfix_add([i for i in coef if i!=0])
                # On converti en Expression
                coef_exp = Expression(postfix_add)

                with Expression.tmp_render():
                    coef_steps = list(coef_exp.simplify().explain())

                #print('\t 1.coef_steps -> ', coef_steps)

            elif type(coef) == Expression:

                with Expression.tmp_render():
                    coef_steps = list(coef.simplify().explain())

                #print('\t 2.coef_steps -> ', coef_steps)

            else:
                try:
                    with Expression.tmp_render():
                        coef_steps += coef.simplify().explain()
                except AttributeError:
                    coef_steps = [coef]

                #print('\t 3.coef_steps -> ', coef_steps)
            # On ajoute toutes ces étapes
            coefs_steps.append(coef_steps)

        #print('\t coefs_steps -> ', coefs_steps)

        # On retourne la matrice
        steps = []
        for coefs in transpose_fill(coefs_steps):
            steps.append(AbstractPolynom(coefs, self._letter))

        ans, steps = steps[-1], steps[:-1]
        ans.steps = steps
            
        return ans

    def simplify(self):
        """Same as reduce """
        return self.reduce()

    @staticmethod
    def postfix_add(numbers):
        """Convert a list of numbers into a postfix addition
        
        :numbers: list of numbers
        :returns: Postfix list of succecive attition of number

        >>> AbstractPolynom.postfix_add([1])
        [1]
        >>> AbstractPolynom.postfix_add([1, 2])
        [1, 2, '+']
        >>> AbstractPolynom.postfix_add([1, 2, 3])
        [1, 2, '+', 3, '+']
        >>> AbstractPolynom.postfix_add(1)
        [1]
        >>> AbstractPolynom.postfix_add([])
        [0]
        """
        if not type(numbers) == list:
            return [numbers]
        elif numbers == []:
            return [0]
        else:
            ans = [[a, op.add] if i!=0 else [a] for (i,a) in enumerate(numbers)]
            return list(chain.from_iterable(ans))
            
    def __eq__(self, other):
        try:
            o_poly = self.conv2poly(other)
            return self._coef == o_poly._coef
        except TypeError:
            return 0

    def __add__(self, other):
        """ Overload + 

        >>> P = AbstractPolynom([1,2,3])
        >>> Q = AbstractPolynom([4,5])
        >>> R = P+Q
        >>> R
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [5, 7, 3]>
        >>> R.steps
        [< <class 'pymath.expression.Expression'> [3, 'x', 2, '^', '*', 2, 'x', '*', '+', 1, '+', 5, 'x', '*', 4, '+', '+'] >, < <class 'pymath.abstract_polynom.AbstractPolynom'> [< <class 'pymath.expression.Expression'> [1, 4, '+'] >, < <class 'pymath.expression.Expression'> [2, 5, '+'] >, 3]>]
        """
        o_poly = self.conv2poly(other)

        n_coef = spe_zip(self._coef, o_poly._coef)
        p = AbstractPolynom(n_coef, letter = self._letter)

        ini_step = [Expression(self.postfix_tokens + o_poly.postfix_tokens + [op.add])]
        ans = p.simplify()
        ans.steps = ini_step + ans.steps
        return ans

    def __radd__(self, other):
        o_poly = self.conv2poly(other)
        return o_poly.__add__(self)

    def __neg__(self):
        """ overload - (as arity 1 operator)

        >>> P = AbstractPolynom([1,2,3])
        >>> Q = -P
        >>> Q
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [-1, -2, -3]>
        >>> Q.steps
        [< <class 'pymath.expression.Expression'> [3, 'x', 2, '^', '*', 2, 'x', '*', '+', 1, '+', '-'] >]
        """
        ini_step = [Expression(self.postfix_tokens + [op.sub1])]
        ans = AbstractPolynom([-i for i in self._coef], letter = self._letter).simplify()
        ans.steps = ini_step + ans.steps
        return ans

    def __sub__(self, other):
        """ overload -

        >>> P = AbstractPolynom([1,2,3])
        >>> Q = AbstractPolynom([4,5,6])
        >>> R = P - Q
        >>> R
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [-3, -3, -3]>
        >>> R.steps
        [< <class 'pymath.expression.Expression'> [3, 'x', 2, '^', '*', 2, 'x', '*', '+', 1, '+', 6, 'x', 2, '^', '*', 5, 'x', '*', '+', 4, '+', '-'] >, < <class 'pymath.expression.Expression'> [3, 'x', 2, '^', '*', 2, 'x', '*', '+', 1, '+', 6, 'x', 2, '^', '*', '-', 5, 'x', '*', '-', 4, '-', '+'] >, < <class 'pymath.abstract_polynom.AbstractPolynom'> [< <class 'pymath.expression.Expression'> [1, -4, '+'] >, < <class 'pymath.expression.Expression'> [2, -5, '+'] >, < <class 'pymath.expression.Expression'> [3, -6, '+'] >]>]
        >>> for i in R.explain():
        ...     print(i)
        3 x^{  2 } + 2 x + 1 - ( 6 x^{  2 } + 5 x + 4 )
        3 x^{  2 } + 2 x + 1 -  6 x^{  2 } - 5 x - 4
        ( 3 - 6 ) x^{  2 } + ( 2 - 5 ) x + 1 - 4
        - 3 x^{  2 } - 3 x - 3
        """
        o_poly = self.conv2poly(other)
        ini_step = [Expression(self.postfix_tokens + o_poly.postfix_tokens + [op.sub])]
        o_poly = -o_poly
        #ini_step += o_poly.steps

        ans = self + o_poly
        ans.steps = ini_step + ans.steps

        return ans

    def __rsub__(self, other):
        o_poly = self.conv2poly(other)
        
        return o_poly.__sub__(self)
    
    def __mul__(self, other):
        """ Overload *

        >>> p = AbstractPolynom([1,2])
        >>> p*3
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [3, 6]>
        >>> (p*3).steps
        [[< <class 'pymath.expression.Expression'> [2, 'x', '*', 1, '+', 3, '*'] >], < <class 'pymath.abstract_polynom.AbstractPolynom'> [3, < <class 'pymath.expression.Expression'> [2, 3, '*'] >]>]
        >>> q = AbstractPolynom([0,0,4])
        >>> q*3
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 0, 12]>
        >>> (q*3).steps
        [[< <class 'pymath.expression.Expression'> [4, 'x', 2, '^', '*', 3, '*'] >], < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 0, < <class 'pymath.expression.Expression'> [4, 3, '*'] >]>]
        >>> r = AbstractPolynom([0,1])
        >>> r*3
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 3]>
        >>> (r*3).steps
        [[< <class 'pymath.expression.Expression'> ['x', 3, '*'] >]]
        >>> p*q
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 0, 4, 8]>
        >>> (p*q).steps
        [[< <class 'pymath.expression.Expression'> [2, 'x', '*', 1, '+', 4, 'x', 2, '^', '*', '*'] >], < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 0, 4, < <class 'pymath.expression.Expression'> [2, 4, '*'] >]>]
        >>> p*r
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 1, 2]>
        >>> P = AbstractPolynom([1,2,3])
        >>> Q = AbstractPolynom([4,5,6])
        >>> P*Q
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [4, 13, 28, 27, 18]>
        """
        # TODO: Je trouve qu'elle grille trop d'étapes... |ven. févr. 27 19:08:44 CET 2015
        o_poly = self.conv2poly(other)

        coefs = [0]*(self.degree + o_poly.degree + 1)
        for (i,a) in enumerate(self._coef):
            for (j,b) in enumerate(o_poly._coef):
                if a == 0 or b == 0:
                    elem = 0
                elif a==1:
                    elem = b
                elif b==1:
                    elem = a
                else:
                    elem = Expression([a, b, op.mul])

                if coefs[i+j]==0:
                    coefs[i+j] = elem
                elif elem != 0:
                    if type(coefs[i+j]) == list:
                        coefs[i+j] += [elem]
                    else:
                        coefs[i+j] = [coefs[i+j] , elem]

        p = AbstractPolynom(coefs, letter = self._letter)
        ini_step = [Expression(self.postfix_tokens + o_poly.postfix_tokens + [op.mul])]
        ans = p.simplify()

        ans.steps = [ini_step] + ans.steps
        return ans

    def __rmul__(self, other):
        o_poly = self.conv2poly(other)

        return o_poly.__mul__(self)
        
    @power_cache
    def __pow__(self, power):
        """ Overload **

        >>> p = AbstractPolynom([0,0,3])
        >>> p**2
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 0, 0, 0, 9]>
        >>> (p**2).steps
        [< <class 'pymath.expression.Expression'> [3, 'x', 2, '^', '*', 2, '^'] >, < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 0, 0, 0, < <class 'pymath.expression.Expression'> [3, 2, '^'] >]>]
        >>> p = AbstractPolynom([1,2])
        >>> p**2
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [1, 4, 4]>
        >>> (p**2).steps
        [< <class 'pymath.expression.Expression'> [2, 'x', '*', 1, '+', 2, '^'] >, [< <class 'pymath.expression.Expression'> [2, 'x', '*', 1, '+', 2, 'x', '*', 1, '+', '*'] >], < <class 'pymath.abstract_polynom.AbstractPolynom'> [1, < <class 'pymath.expression.Expression'> [2, 2, '+'] >, < <class 'pymath.expression.Expression'> [2, 2, '*'] >]>]
        >>> p = AbstractPolynom([0,0,1])
        >>> p**3
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [0, 0, 0, 0, 0, 0, 1]>
        >>> p = AbstractPolynom([1,2,3])
        >>> p**2
        < <class 'pymath.abstract_polynom.AbstractPolynom'> [1, 4, 10, 12, 9]>

        """
        if not type(power):
            raise ValueError("Can't raise {obj} to {pw} power".format(obj = self.__class__, pw = str(power)))

        ini_step = [Expression(self.postfix_tokens + [power, op.pw])]

        if self.is_monom():
            if self._coef[self.degree] == 1:
                coefs = [0]*self.degree*power + [1]
                p = AbstractPolynom(coefs, letter = self._letter)
                ans = p
            else:
                coefs = [0]*self.degree*power + [Expression([self._coef[self.degree] , power, op.pw])]
                p = AbstractPolynom(coefs, letter = self._letter)
                ans = p.simplify()
        else:
            if power == 2:
                ans = self * self
            else:
                # TODO: faudrait changer ça c'est pas très sérieux |ven. févr. 27 22:08:00 CET 2015
                raise AttributeError("__pw__ not implemented yet when power is greatter than 2")

        ans.steps = ini_step + ans.steps
        return ans

    def __xor__(self, power):
        return self.__pow__(power)



# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 