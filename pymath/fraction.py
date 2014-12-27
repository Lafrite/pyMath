#!/usr/bin/env python
# encoding: utf-8

from .arithmetic import gcd
from .generic import isNumber
from .operator import op
from .expression import Expression
from .render import txt, tex


__all__ = ['Fraction']

class Fraction(object):
    """Fractions!"""

    def __init__(self, num, denom = 1):
        """To initiate a fraction we need a numerator and a denominator

        :param num: the numerator
        :param denom: the denominator

        """
        self._num = num
        self._denom = denom

        self.isNumber = 1

    def simplify(self):
        """Simplify the fraction 

        :returns: steps to simplify the fraction or the fraction if there is nothing to do

        >>> f = Fraction(3, 6)
        >>> f.simplify()
        [< Expression [1, 3, '*', 2, 3, '*', '/']>, < Fraction 1 / 2>]
        >>> f = Fraction(0,3)
        >>> f.simplify()
        [0]

        """
        steps = []

        if self._num == 0:
            steps.append(0)

            return steps

        if self._denom < 0:
            n_frac = Fraction(-self._num, -self._denom)
            steps.append(n_frac)
        else: 
            n_frac = self

        gcd_ = gcd(abs(n_frac._num), abs(n_frac._denom))
        if gcd_ == n_frac._denom:
            n_frac = n_frac._num // gcd_
            steps.append(n_frac)

        elif gcd_ != 1:
            n_frac = Fraction(n_frac._num // gcd_ , n_frac._denom // gcd_)
            steps.append(Expression([n_frac._num, gcd_, op.mul, n_frac._denom, gcd_, op.mul, op.div ]))

            steps.append(n_frac)

        return steps

    @property
    def postfix(self):
        """Postfix form of the fraction

        >>> f = Fraction(3, 5)
        >>> f.postfix
        [3, 5, '/']

        """
        if self._denom == 1:
            return [self._num]
        else:
            return [self._num, self._denom, op.div]

    def __str__(self):
        return str(Expression(self.postfix))

    def __repr__(self):
        return "< Fraction {num} / {denom}>".format(num=self._num, denom = self._denom)

    def __txt__(self):
        old_render = Expression.get_render()
        Expression.set_render(txt)
        _txt = self.__str__()
        Expression.set_render(old_render)

        return _txt

    def __tex__(self):
        old_render = Expression.get_render()
        Expression.set_render(tex)
        _txt = self.__str__()
        Expression.set_render(old_render)

        return _txt

    def __float__(self):
        return self._num / self._denom

    def convert2fraction(self, other):
        """ Convert a other into a fraction """
        if type(other) == Fraction:
            #cool
            number = other
        else:
            number = Fraction(other)

        return number
    
    def __add__(self, other):
        """ overload +

        >>> f = Fraction(1, 2)
        >>> g = Fraction(2, 3)
        >>> f + g
        [< Expression [1, 3, '*', 2, 3, '*', '/', 2, 2, '*', 3, 2, '*', '/', '+']>, < Expression [3, 4, '+', 6, '/']>, < Fraction 7 / 6>]
        >>> f + 2
        [< Expression [1, 1, '*', 2, 1, '*', '/', 2, 2, '*', 1, 2, '*', '/', '+']>, < Expression [1, 4, '+', 2, '/']>, < Fraction 5 / 2>]
        >>> f = Fraction(3, 4)
        >>> g = Fraction(5, 4)
        >>> f + g
        [< Expression [3, 5, '+', 4, '/']>, < Fraction 8 / 4>, 2]

        """

        if other == 0:
            return [self]

        number = self.convert2fraction(other)

        steps = []

        if self._denom == number._denom:
            com_denom = self._denom
            num1 = self._num
            num2 = number._num

        else:
            gcd_denom = gcd(self._denom, number._denom)
            coef1 = number._denom // gcd_denom
            coef2 = self._denom // gcd_denom

            steps.append(Expression([self._num, coef1, op.mul, self._denom, coef1, op.mul, op.div, number._num, coef2, op.mul, number._denom, coef2, op.mul, op.div,op.add]) )

            com_denom = self._denom * coef1
            num1 = self._num * coef1
            num2 = number._num * coef2

        steps.append(Expression([num1, num2, op.add, com_denom, op.div]))

        num = num1 + num2

        ans_frac = Fraction(num, com_denom)
        steps.append(ans_frac)
        steps += ans_frac.simplify()

        return steps

    def __radd__(self, other):
        if other == 0:
            return [self]

        number = self.convert2fraction(other)

        return number + self

    def __sub__(self, other):
        """ overload -

        >>> f = Fraction(1, 2)
        >>> g = Fraction(2, 3)
        >>> f - g
        [< Expression [1, 3, '*', 2, 3, '*', '/', 2, 2, '*', 3, 2, '*', '/', '-']>, < Expression [3, 4, '-', 6, '/']>, < Fraction -1 / 6>]

        """
        if other == 0:
            return [self]

        number = self.convert2fraction(other)

        steps = []

        if self._denom == number._denom:
            com_denom = self._denom
            num1 = self._num
            num2 = number._num

        else:
            gcd_denom = gcd(self._denom, number._denom)
            coef1 = number._denom // gcd_denom
            coef2 = self._denom // gcd_denom

            steps.append(Expression([self._num, coef1, op.mul, self._denom, coef1, op.mul, op.div, number._num, coef2, op.mul, number._denom, coef2, op.mul, op.div,op.sub]))

            com_denom = self._denom * coef1
            num1 = self._num * coef1
            num2 = number._num * coef2

        steps.append(Expression([num1, num2, op.sub, com_denom, op.div]))

        num = num1 - num2

        ans_frac = Fraction(num, com_denom)
        steps.append(ans_frac)
        steps += ans_frac.simplify()

        return steps

    def __rsub__(self, other):
        if other == 0:
            return [self]

        number = self.convert2fraction(other)

        return number - self

    def __neg__(self):
        """ overload - (as arity 1 operator

        >>> f = Fraction(1, 2)
        >>> -f
        [< Fraction -1 / 2>]
        >>> f = Fraction(1, -2)
        >>> f
        < Fraction 1 / -2>
        >>> -f
        [< Fraction -1 / -2>, < Fraction 1 / 2>]

        """
        f = Fraction(-self._num, self._denom)
        return [f] + f.simplify()
    
    def __mul__(self, other):
        """ overload *

        >>> f = Fraction(1, 2)
        >>> g = Fraction(2, 3)
        >>> f*g
        [< Expression [1, 1, 2, '*', '*', 1, 2, '*', 3, '*', '/']>, < Fraction 1 / 3>]
        >>> f * 0
        [0]
        >>> f*1
        [< Fraction 1 / 2>]
        >>> f*4
        [< Expression [1, 2, '*', 2, '*', 1, 2, '*', '/']>, < Fraction 2 / 1>, 2]

        """
        steps = []

        if other == 0:
            return [0]
        elif other == 1:
            return [self]

        elif type(other) == int:
            gcd1 = gcd(other, self._denom)
            if gcd1 != 1:
                num = [self._num, int(other/gcd1), op.mul, gcd1,op.mul]
                denom = [int(self._denom/gcd1), gcd1, op.mul]
            else:
                num = [self._num, other, op.mul]
                denom = [self._denom]
            steps.append(Expression(num + denom + [op.div]))

            num = int(self._num * other / gcd1)
            denom = int(self._denom / gcd1)

        else:
            number = self.convert2fraction(other)

            gcd1 = gcd(self._num, number._denom) 
            if gcd1 != 1:
                num1 = [int(self._num/ gcd1), gcd1, op.mul]
                denom2 = [int(number._denom/ gcd1), gcd1, op.mul] 
            else:
                num1 = [self._num]
                denom2 = [number._denom]

            gcd2 = gcd(self._denom, number._num) 
            if gcd2 != 1:
                num2 = [int(number._num/ gcd2), gcd2, op.mul]
                denom1 = [int(self._denom/ gcd2), gcd2, op.mul] 
            else:
                num2 = [number._num]
                denom1 = [self._denom]


            steps.append(Expression(num1 +  num2 + [ op.mul] +  denom1 +  denom2 + [op.mul, op.div]))

            num = int(self._num * number._num / (gcd1 * gcd2))
            denom = int(self._denom * number._denom / (gcd1 * gcd2))

        ans_frac = Fraction(num, denom)
        steps.append(ans_frac)
        steps += ans_frac.simplify()

        return steps

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("division by zero")
        elif other == 1:
            return [self]

        number = self.convert2fraction(other)

        steps = []
        number = Fraction(number._denom, number._num)
        steps.append(Expression([self, number, op.mul]))
        steps += self * number

        return steps

    def __rtruediv__(self, other):
        number = self.convert2fraction(other)

        return number / self

    def __pow__(self, power):
        """ overload **
        
        >>> f = Fraction(3, 4)
        >>> f**0
        [1]
        >>> f**1
        [< Fraction 3 / 4>]
        >>> f**3
        [< Expression [3, 3, '^', 4, 3, '^', '/']>, < Fraction 27 / 64>]
        >>> f = Fraction(6, 4)
        >>> f**3
        [< Expression [6, 3, '^', 4, 3, '^', '/']>, < Fraction 216 / 64>, < Expression [27, 8, '*', 8, 8, '*', '/']>, < Fraction 27 / 8>]
        
        """
        if not type(power) == int:
            raise ValueError("Can't raise fraction to power {}".format(str(power)))

        if power == 0:
            return [1]
        elif power == 1:
            return [self]
        else:
            steps = [Expression([self._num, power, op.pw, self._denom, power, op.pw, op.div])]
            ans_frac = Fraction(self._num ** power, self._denom ** power)
            steps.append(ans_frac)
            steps += ans_frac.simplify()
            return steps

    def __xor__(self, power):
        """ overload ^


        >>> f = Fraction(3, 4)
        >>> f^0
        [1]
        >>> f^1
        [< Fraction 3 / 4>]
        >>> f^3
        [< Expression [3, 3, '^', 4, 3, '^', '/']>, < Fraction 27 / 64>]
        >>> f = Fraction(6, 4)
        >>> f^3
        [< Expression [6, 3, '^', 4, 3, '^', '/']>, < Fraction 216 / 64>, < Expression [27, 8, '*', 8, 8, '*', '/']>, < Fraction 27 / 8>]
        
        """
        
        return self.__pow__(power)

    def __abs__(self):
        return Fraction(abs(self._num), abs(self._denom))

    def __eq__(self, other):
        """ == """
        if isNumber(other):
            number = self.convert2fraction(other)

            return self._num * number._denom == self._denom * number._num
        else:
            return 0

    def __lt__(self, other):
        """ < """
        return float(self) < float(other)

    def __le__(self, other):
        """ <= """
        return float(self) <= float(other)

    def __gt__(self, other):
        """ > """
        return float(self) > float(other)

    def __ge__(self, other):
        """ >= """
        return float(self) >= float(other)



if __name__ == '__main__':
    #f = Fraction(1, 12)
    #g = Fraction(1, 12)
    #h = Fraction(1,-5)
    #t = Fraction(10,3)
    #print("---------")
    #print("1 + ", str(h))
    #for i in (1 + h):
    #    print(i)
    #print("---------")
    #print(str(f) , "+", str(t))
    #for i in (f + t):
    #    print(i)
    #print("---------")
    #print(str(f) , "+", str(g))
    #for i in (f + g):
    #    print(i)
    #print("---------")
    #print(str(f) , "-", str(g))
    #for i in (f - g):
    #    print(i)
    #print("---------")
    #print(str(f) , "*", str(g))
    #for i in (f * g):
    #    print(i)
    #print("---------")
    #print(str(h) , "+", str(t))
    #for i in (h + t):
    #    print(i)
    #print("---------")
    #print(str(h) , "-", str(t))
    #for i in (h - t):
    #    print(i)
    #print("---------")
    #print(str(h) , "*", str(t))
    #for i in (h * t):
    #    print(i)
    #print("---------")
    #print("-", str(h) )
    #for i in (-h):
    #    print(i)
    #print("---------")
    #print(str(h) , "/", str(t))
    #for i in (h / t):
    #    print(i)
    #print("---------")
    #print(str(h) , "+", str(0))
    #for i in (h + 0):
    #    print(i)
    #print("---------")
    #print(str(h) , "*", str(1))
    #for i in (h * 1):
    #    print(i)
    #print("---------")
    #print(str(h) , "*", str(0))
    #for i in (h * 0):
    #    print(i)
    #print("---------")
    #print(str(h) , "*", str(4))
    #for i in (h * 4):
    #    print(i)

    #print(f.simplify())

    import doctest
    doctest.testmod()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
