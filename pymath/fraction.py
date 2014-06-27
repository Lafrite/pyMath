#!/usr/bin/env python
# encoding: utf-8

from .arithmetic import gcd

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

    def simplify(self):
        """Simplify the fraction 

        :returns: steps to simplify the fraction or the fraction if there is nothing to do
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
        if n_frac._num == n_frac._denom:
            n_frac = Fraction(1,1)
            steps.append(n_frac)

        elif gcd_ != 1:
            n_frac = Fraction(n_frac._num // gcd_ , n_frac._denom // gcd_)
            steps.append([n_frac._num, gcd_, '*', n_frac._denom, gcd_, '*', '/' ])

            steps.append(n_frac)

        return steps

    def __str__(self):
        if self._denom == 1:
            return str(self._num)
        else:
            return str(self._num) + " / " + str(self._denom)

    def __repr__(self):
        return "< Fraction " + self.__str__() + ">"

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

            steps.append([self._num, coef1, "*", self._denom, coef1, "*", '/', number._num, coef2, "*", number._denom, coef2, "*", "/",'+']) 

            com_denom = self._denom * coef1
            num1 = self._num * coef1
            num2 = number._num * coef2

        steps.append([num1, num2, '+', com_denom, '/'])

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

            steps.append([self._num, coef1, "*", self._denom, coef1, "*", '/', number._num, coef2, "*", number._denom, coef2, "*", "/",'-']) 

            com_denom = self._denom * coef1
            num1 = self._num * coef1
            num2 = number._num * coef2

        steps.append([num1, num2, '-', com_denom, '/'])

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
        return Fraction(-self._num,self._denom).simplify()
    
    def __mul__(self, other):
        steps = []

        if other == 0:
            return [0]
        elif other == 1:
            return [self]

        elif type(other) == int:
            gcd1 = gcd(other, self._denom)
            if gcd1 != 1:
                num = [self._num, int(other/gcd1), "*", gcd1,"*"]
                denom = [int(self._denom/gcd1), gcd1, "*"]
            else:
                num = [self._num, other, "*"]
                denom = [self._denom]
            steps.append(num + denom + ["/"])

            num = int(self._num * other / gcd1)
            denom = int(self._denom / gcd1)

        else:
            number = self.convert2fraction(other)

            gcd1 = gcd(self._num, number._denom) 
            if gcd1 != 1:
                num1 = [int(self._num/ gcd1), gcd1, "*"]
                denom2 = [int(number._denom/ gcd1), gcd1, "*"] 
            else:
                num1 = [self._num]
                denom2 = [number._denom]

            gcd2 = gcd(self._denom, number._num) 
            if gcd2 != 1:
                num2 = [int(number._num/ gcd2), gcd2, "*"]
                denom1 = [int(self._denom/ gcd2), gcd2, "*"] 
            else:
                num2 = [number._num]
                denom1 = [self._denom]


            steps.append(num1 +  num2 + [ '*'] +  denom1 +  denom2 + ['*', '/'])

            num = int(self._num * number._num / (gcd1 * gcd2))
            denom = int(self._denom * number._denom / (gcd1 * gcd2))

        ans_frac = Fraction(num, denom)
        steps.append(ans_frac)
        steps += ans_frac.simplify()

        return steps

    def __rmul__(self, other):
        number = self.convert2fraction(other)

        return number * self

    def __truediv__(self, other):
        if other == 0:
            raise ZeroDivisionError("division by zero")
        elif other == 1:
            return [self]

        number = self.convert2fraction(other)

        steps = []
        number = Fraction(number._denom, number._num)
        steps.append([self, number, "*"])
        steps += self * number

        return steps

    def __rtruediv__(self, other):
        number = self.convert2fraction(other)

        return number / self

    def __abs__(self):
        return Fraction(abs(self._num), abs(self._denom))

    def __eq__(self, other):
        """ == """
        number = self.convert2fraction(other)

        return self._num * number._denom == self._denom * number._num

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
    f = Fraction(1, 12)
    g = Fraction(1, 12)
    h = Fraction(1,-5)
    t = Fraction(10,3)
    print("---------")
    print("1 + ", str(h))
    for i in (1 + h):
        print(i)
    print("---------")
    print(str(f) , "+", str(t))
    for i in (f + t):
        print(i)
    print("---------")
    print(str(f) , "+", str(g))
    for i in (f + g):
        print(i)
    print("---------")
    print(str(f) , "-", str(g))
    for i in (f - g):
        print(i)
    print("---------")
    print(str(f) , "*", str(g))
    for i in (f * g):
        print(i)
    print("---------")
    print(str(h) , "+", str(t))
    for i in (h + t):
        print(i)
    print("---------")
    print(str(h) , "-", str(t))
    for i in (h - t):
        print(i)
    print("---------")
    print(str(h) , "*", str(t))
    for i in (h * t):
        print(i)
    print("---------")
    print("-", str(h) )
    for i in (-h):
        print(i)
    print("---------")
    print(str(h) , "/", str(t))
    for i in (h / t):
        print(i)
    print("---------")
    print(str(h) , "+", str(0))
    for i in (h + 0):
        print(i)
    print("---------")
    print(str(h) , "*", str(1))
    for i in (h * 1):
        print(i)
    print("---------")
    print(str(h) , "*", str(0))
    for i in (h * 0):
        print(i)
    print("---------")
    print(str(h) , "*", str(4))
    for i in (h * 4):
        print(i)

    #print(f.simplify())

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
