#!/usr/bin/env python
# encoding: utf-8

from .arithmetic import gcd
from .generic import isNumber
from .operator import op
from .expression import Expression
from .explicable import Explicable
from .render import txt, tex
from copy import copy


__all__ = ['Fraction']

class Fraction(Explicable):
    """Fractions!"""

    def __init__(self, num, denom = 1):
        """To initiate a fraction we need a numerator and a denominator

        :param num: the numerator
        :param denom: the denominator

        """
        super(Fraction, self).__init__()
        self._num = num
        self._denom = denom

        self.isNumber = 1

    def simplify(self):
        """Simplify the fraction 

        :returns: steps to simplify the fraction or the fraction if there is nothing to do

        >>> f = Fraction(3, 6)
        >>> f.simplify()
        < Fraction 1 / 2>
        >>> for i in f.simplify().explain():
        ...     print(i)
        \\frac{ 3 }{ 6 }
        \\frac{ 1 \\times 3 }{ 2 \\times 3 }
        \\frac{ 1 }{ 2 }
        >>> f = Fraction(6,9)
        >>> f.simplify()
        < Fraction 2 / 3>
        >>> for i in f.simplify().explain():
        ...     print(i)
        \\frac{ 6 }{ 9 }
        \\frac{ 2 \\times 3 }{ 3 \\times 3 }
        \\frac{ 2 }{ 3 }
        >>> f = Fraction(0,3)
        >>> f.simplify()
        0

        """
        ini_step = [Expression(self.postfix_tokens)]

        if self._num == 0:
            return Expression([0])

        elif self._denom < 0:
            n_frac = Fraction(-self._num, -self._denom)
            ans = n_frac.simplify()
            ans.steps = ini_step + ans.steps
            return ans

        gcd_ = gcd(abs(self._num), abs(self._denom))
        if gcd_ == self._denom:
            n_frac = self._num // gcd_
            return Expression([n_frac])

        elif gcd_ != 1:
            n_frac = Fraction(self._num // gcd_ , self._denom // gcd_)
            ini_step += [Expression([n_frac._num, gcd_, op.mul, n_frac._denom, gcd_, op.mul, op.div ])]

            n_frac.steps = ini_step + n_frac.steps
            return n_frac

        else:
            return copy(self)

    @property
    def postfix_tokens(self):
        """Postfix form of the fraction

        >>> f = Fraction(3, 5)
        >>> f.postfix_tokens
        [3, 5, '/']

        """
        if self._denom == 1:
            return [self._num]
        else:
            return [self._num, self._denom, op.div]

    def __str__(self):
        return str(Expression(self.postfix_tokens))

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
        _tex = self.__str__()
        Expression.set_render(old_render)

        return _tex

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
        < Fraction 7 / 6>
        >>> print("\\n".join([repr(i) for i in (f+g).steps]))
        < <class 'pymath.expression.Expression'> [1, 2, '/', 2, 3, '/', '+'] >
        < <class 'pymath.expression.Expression'> [1, 3, '*', 2, 3, '*', '/', 2, 2, '*', 3, 2, '*', '/', '+'] >
        < <class 'pymath.expression.Expression'> [3, 6, '/', 4, 6, '/', '+'] >
        < <class 'pymath.expression.Expression'> [< Fraction 3 / 6>, < Fraction 4 / 6>, '+'] >
        < <class 'pymath.expression.Expression'> [3, 6, '/', 4, 6, '/', '+'] >
        < <class 'pymath.expression.Expression'> [3, 4, '+', 6, '/'] >
        >>> f + 2
        < Fraction 5 / 2>
        >>> print("\\n".join([repr(i) for i in (f+2).steps]))
        < <class 'pymath.expression.Expression'> [1, 2, '/', 2, '+'] >
        < <class 'pymath.expression.Expression'> [1, 1, '*', 2, 1, '*', '/', 2, 2, '*', 1, 2, '*', '/', '+'] >
        < <class 'pymath.expression.Expression'> [1, 2, '/', 4, 2, '/', '+'] >
        < <class 'pymath.expression.Expression'> [< Fraction 1 / 2>, < Fraction 4 / 2>, '+'] >
        < <class 'pymath.expression.Expression'> [1, 2, '/', 4, 2, '/', '+'] >
        < <class 'pymath.expression.Expression'> [1, 4, '+', 2, '/'] >
        >>> f = Fraction(3, 4)
        >>> g = Fraction(5, 4)
        >>> f + g
        2
        >>> print("\\n".join([repr(i) for i in (f+g).steps]))
        < <class 'pymath.expression.Expression'> [3, 4, '/', 5, 4, '/', '+'] >
        < <class 'pymath.expression.Expression'> [3, 5, '+', 4, '/'] >
        >>> f+0
        < Fraction 3 / 4>
        >>> (f+0).steps
        []

        """

        if other == 0:
            return copy(self)

        number = self.convert2fraction(other)

        if self._denom == number._denom:
            com_denom = self._denom
            num1 = self._num
            num2 = number._num

            exp = Expression([num1, num2, op.add, com_denom, op.div])

        else:
            gcd_denom = gcd(self._denom, number._denom)
            coef1 = number._denom // gcd_denom
            coef2 = self._denom // gcd_denom

            exp = Expression([self._num, coef1, op.mul, self._denom, coef1, op.mul, op.div, number._num, coef2, op.mul, number._denom, coef2, op.mul, op.div,op.add])

        ans = exp.simplify()
        ini_step = Expression(self.postfix_tokens + number.postfix_tokens + [op.add])
        ans.steps = [ini_step] + ans.steps
        #print("\t\tIn add ans.steps -> ", ans.steps)
        return ans

    def __radd__(self, other):
        if other == 0:
            return Expression(self.postfix_tokens)

        number = self.convert2fraction(other)

        return number + self

    def __sub__(self, other):
        """ overload -

        >>> f = Fraction(1, 2)
        >>> g = Fraction(2, 3)
        >>> f - g
        < Fraction -1 / 6>
        >>> print("\\n".join([repr(i) for i in (f-g).steps]))
        < <class 'pymath.expression.Expression'> [1, 2, '/', 2, 3, '/', '-'] >
        < <class 'pymath.expression.Expression'> [1, 3, '*', 2, 3, '*', '/', 2, 2, '*', 3, 2, '*', '/', '-'] >
        < <class 'pymath.expression.Expression'> [3, 6, '/', 4, 6, '/', '-'] >
        < <class 'pymath.expression.Expression'> [< Fraction 3 / 6>, < Fraction 4 / 6>, '-'] >
        < <class 'pymath.expression.Expression'> [3, 6, '/', 4, 6, '/', '-'] >
        < <class 'pymath.expression.Expression'> [3, 4, '-', 6, '/'] >
        >>> f - 0
        < Fraction 1 / 2>
        >>> (f-0).steps
        []

        """
        if other == 0:
            return copy(self)

        number = self.convert2fraction(other)

        if self._denom == number._denom:
            com_denom = self._denom
            num1 = self._num
            num2 = number._num

            exp = Expression([num1, num2, op.sub, com_denom, op.div])

        else:
            gcd_denom = gcd(self._denom, number._denom)
            coef1 = number._denom // gcd_denom
            coef2 = self._denom // gcd_denom

            exp = Expression([self._num, coef1, op.mul, self._denom, coef1, op.mul, op.div, number._num, coef2, op.mul, number._denom, coef2, op.mul, op.div,op.sub])

        ini_step = Expression(self.postfix_tokens + number.postfix_tokens + [op.sub])
        ans = exp.simplify()
        ans.steps = [ini_step] + ans.steps
        return ans

    def __rsub__(self, other):
        if other == 0:
            return copy(self)

        number = self.convert2fraction(other)

        return number - self

    def __neg__(self):
        """ overload - (as arity 1 operator)

        >>> f = Fraction(1, 2)
        >>> -f
        < Fraction -1 / 2>
        >>> (-f).steps
        []
        >>> f = Fraction(1, -2)
        >>> f
        < Fraction 1 / -2>
        >>> -f
        < Fraction 1 / 2>
        >>> (-f).steps
        [< <class 'pymath.expression.Expression'> [-1, -2, '/'] >]

        """
        f = Fraction(-self._num, self._denom)
        ans =  f.simplify()

        return ans
    
    def __mul__(self, other):
        """ overload *

        >>> f = Fraction(1, 2)
        >>> g = Fraction(2, 3)
        >>> f*g
        < Fraction 1 / 3>
        >>> print("\\n".join([repr(i) for i in (f*g).steps]))
        < <class 'pymath.expression.Expression'> [1, 2, '/', 2, 3, '/', '*'] >
        < <class 'pymath.expression.Expression'> [1, 1, 2, '*', '*', 1, 2, '*', 3, '*', '/'] >
        < <class 'pymath.expression.Expression'> [1, 2, '*', 2, 3, '*', '/'] >
        < <class 'pymath.expression.Expression'> [2, 6, '/'] >
        < <class 'pymath.expression.Expression'> [1, 2, '*', 3, 2, '*', '/'] >
        >>> f * 0
        0
        >>> (f*0).steps
        []
        >>> f*1
        < Fraction 1 / 2>
        >>> (f*1).steps
        []
        >>> f*4
        2
        >>> print("\\n".join([repr(i) for i in (f*4).steps]))
        < <class 'pymath.expression.Expression'> [1, 2, '/', 4, '*'] >
        < <class 'pymath.expression.Expression'> [1, 2, '*', 2, '*', 1, 2, '*', '/'] >
        < <class 'pymath.expression.Expression'> [2, 2, '*', 2, '/'] >

        """
        steps = []

        if other == 0:
            return Expression([0])
        elif other == 1:
            return copy(self)

        # TODO: Changer dans le cas où il y a trop de 1 |dim. déc. 28 10:44:10 CET 2014

        elif type(other) == int:
            gcd1 = gcd(other, self._denom)
            if gcd1 != 1:
                num = [self._num, int(other/gcd1), op.mul, gcd1,op.mul]
                denom = [int(self._denom/gcd1), gcd1, op.mul]
            else:
                num = [self._num, other, op.mul]
                denom = [self._denom]

            exp = Expression(num + denom + [op.div])
            ini_step = Expression(self.postfix_tokens + [other, op.mul])

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


            exp = Expression(num1 +  num2 + [ op.mul] +  denom1 +  denom2 + [op.mul, op.div])

            ini_step = Expression(self.postfix_tokens + number.postfix_tokens + [op.mul])
        ans = exp.simplify()
        ans.steps = [ini_step] + ans.steps
        return ans

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        """ overload /

        >>> f = Fraction(1,2)
        >>> g = Fraction(3,4)
        >>> f / 0
        Traceback (most recent call last):
        ...
        ZeroDivisionError: division by zero
        >>> f / 1
        < Fraction 1 / 2>
        >>> (f/1).steps
        []
        >>> f / g
        < Fraction 2 / 3>

        """
        if other == 0:
            raise ZeroDivisionError("division by zero")
        elif other == 1:
            return copy(self)

        number = self.convert2fraction(other)

        ini_step = Expression(self.postfix_tokens + number.postfix_tokens + [op.div])

        number = Fraction(number._denom, number._num)
        ans = self * number

        ans.steps = [ini_step] + ans.steps
        return ans

    def __rtruediv__(self, other):
        number = self.convert2fraction(other)

        return number / self

    def __pow__(self, power):
        """ overload **
        
        >>> f = Fraction(3, 4)
        >>> f**0
        1
        >>> (f**0).steps
        []
        >>> f**1
        < Fraction 3 / 4>
        >>> (f**1).steps
        []
        >>> f**3
        < Fraction 27 / 64>
        >>> print("\\n".join([repr(i) for i in (f**3).steps]))
        < <class 'pymath.expression.Expression'> [3, 4, '/', 3, '^'] >
        < <class 'pymath.expression.Expression'> [3, 3, '^', 4, 3, '^', '/'] >
        >>> f = Fraction(6, 4)
        >>> f**3
        < Fraction 27 / 8>
        >>> print("\\n".join([repr(i) for i in (f**3).steps]))
        < <class 'pymath.expression.Expression'> [6, 4, '/', 3, '^'] >
        < <class 'pymath.expression.Expression'> [6, 3, '^', 4, 3, '^', '/'] >
        < <class 'pymath.expression.Expression'> [216, 64, '/'] >
        < <class 'pymath.expression.Expression'> [27, 8, '*', 8, 8, '*', '/'] >
        
        """
        if not type(power) == int:
            raise ValueError("Can't raise fraction to power {}".format(str(power)))

        if power == 0:
            return Expression([1])
        elif power == 1:
            return copy(self)
        else:
            ini_step = Expression(self.postfix_tokens + [power, op.pw])
            exp = Expression([self._num, power, op.pw, self._denom, power, op.pw, op.div])

            ans = exp.simplify()
            ans.steps = [ini_step] + ans.steps
            return ans

    def __xor__(self, power):
        """ overload ^

        Work like **

        >>> f = Fraction(3, 4)
        >>> f^0
        1
        >>> f^1
        < Fraction 3 / 4>
        >>> f^3
        < Fraction 27 / 64>
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

    def __copy__(self):
        """ Copying the fraction removing steps where it is from """
        return Fraction(self._num, self._denom)



if __name__ == '__main__':
    f = Fraction(1, 12)
    g = Fraction(6, 12)
    for i in g.simplify().explain():
        print("g = ",i)
    h = Fraction(1,-5)
    t = Fraction(10,3)
    print("---------")
    for i in (0 + h).explain():
        print('0 + h = ',i)
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
