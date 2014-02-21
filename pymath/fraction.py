#!/usr/bin/env python
# encoding: utf-8

from .arithmetic import gcd

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

        if self._denom < 0:
            n_frac = Fraction(-self._num, -self._denom)
            steps.append(n_frac)

        gcd_ = gcd(abs(self._num), abs(self._denom))
        if self._num == self._denom:
            n_frac = Fraction(1,1)
            steps.append(n_frac)

        elif gcd_ != 1:
            n_frac = Fraction(self._num // gcd_ , self._denom // gcd_)
            #steps.append("( {reste1} * {gcd} ) / ( {reste2} * {gcd} )".format(reste1 = n_frac._num, reste2 = n_frac._denom, gcd = gcd_))
            steps.append([n_frac._num, gcd_, '*', n_frac._denom, gcd_, '*', '/' ])

            # Certainement le truc le plus moche que j'ai jamais fait... On ne met que des strings dans steps puis au dernier moment on met une fraction. C'est moche de ma part
            steps.append(n_frac)

        return steps

    def __str__(self):
        if self._denom == 1:
            return str(self._num)
        else:
            return str(self._num) + " / " + str(self._denom)

    def __repr__(self):
        return "< Fraction " + self.__str__() + ">"
    
    def __add__(self, other):
        if type(other) == Fraction:
            #cool
            number = other
        else:
            number = Fraction(other)

        steps = []

        if self._denom == number._denom:
            com_denom = self._denom
            num1 = self._num
            num2 = number._num

        else:
            gcd_denom = gcd(self._denom, number._denom)
            coef1 = number._denom // gcd_denom
            coef2 = self._denom // gcd_denom

            #steps.append("( {num1} * {coef1} ) / ( {den1} * {coef1} ) + ( {num2} * {coef2} ) / ( {den2} * {coef2} )".format(num1 = self._num, den1 = self._denom, coef1 = coef1, num2 = number._num, den2 = number._denom, coef2 = coef2)) 

            steps.append([self._num, coef1, "*", self._denom, coef1, "*", '/', number._num, coef2, "*", number._denom, coef2, "*", "/",'+']) 

            com_denom = self._denom * coef1
            num1 = self._num * coef1
            num2 = number._num * coef2

        #steps.append("( {num1} + {num2} ) / {denom}".format(num1 = num1, num2 = num2, denom = com_denom))

        steps.append([num1, num2, '+', com_denom, '/'])

        num = num1 + num2

        ans_frac = Fraction(num, com_denom)
        steps.append(ans_frac)
        steps += ans_frac.simplify()

        return steps

    def __sub__(self, other):
        if type(other) == Fraction:
            #cool
            number = other
        else:
            number = Fraction(other)

        steps = []

        if self._denom == number._denom:
            com_denom = self._denom
            num1 = self._num
            num2 = number._num

        else:
            gcd_denom = gcd(self._denom, number._denom)
            coef1 = number._denom // gcd_denom
            coef2 = self._denom // gcd_denom

            #steps.append("( {num1} * {coef1} ) / ( {den1} * {coef1} ) - ( {num2} * {coef2} ) / ( {den2} * {coef2} )".format(num1 = self._num, den1 = self._denom, coef1 = coef1, num2 = number._num, den2 = number._denom, coef2 = coef2)) 
            steps.append([self._num, coef1, "*", self._denom, coef1, "*", '/', number._num, coef2, "*", number._denom, coef2, "*", "/",'-']) 

            com_denom = self._denom * coef1
            num1 = self._num * coef1
            num2 = number._num * coef2

        #steps.append("( {num1} - {num2} ) / {denom}".format(num1 = num1, num2 = num2, denom = com_denom))
        steps.append([num1, num2, '-', com_denom, '/'])

        num = num1 - num2

        ans_frac = Fraction(num, com_denom)
        steps.append(ans_frac)
        steps += ans_frac.simplify()

        return steps

    def __neg__(self):
        return [Fraction(-self._num,self._denom)]
    
    def __mul__(self, other):
        if type(other) == Fraction:
            #cool
            number = other
        else:
            number = Fraction(other)

        steps = []
        #steps.append("( {num1} * {num2} ) / ( {denom1} * {denom2} )".format(num1 = self._num, num2 = number._num, denom1 = self._denom, denom2 = number._denom))

        steps.append([self._num, number._num, '*', self._denom, number._denom, '*', '/'])

        num = self._num * number._num
        denom = self._denom * number._denom

        ans_frac = Fraction(num, denom)
        steps.append(ans_frac)
        steps += ans_frac.simplify()

        return steps

    def __truediv__(self, other):
        if type(other) == Fraction:
            #cool
            number = other
        else:
            number = Fraction(other)

        steps = []
        number = Fraction(number._denom, number._num)
        steps += self * number

        return steps

    def __lt__(self, other):
        if type(other) == Fraction:
            return (self._num / self._denom) < (other._num / other._denom)
        else:
            return (self._num / self._denom) < other

    def __le__(self, other):
        if type(other) == Fraction:
            return (self._num / self._denom) <= (other._num / other._denom)
        else:
            return (self._num / self._denom) <= other



if __name__ == '__main__':
    f = Fraction(1, 12)
    g = Fraction(1, 12)
    h = Fraction(-1,5)
    t = Fraction(-4,5)
    print("---------")
    for i in (f - 1):
        print(i)
    print("---------")
    for i in (f + 1):
        print(i)
    print("---------")
    for i in (f + g):
        print(i)
    #print("---------")
    #for i in (f - g):
    #    print(i)
    #print("---------")
    #for i in (f * g):
    #    print(i)
    #print("---------")
    #for i in (h + t):
    #    print(i)
    #print("---------")
    #for i in (h - t):
    #    print(i)
    #print("---------")
    #for i in (h * t):
    #    print(i)
    #print("---------")
    #for i in (h / t):
    #    print(i)

    #print(f.simplify())

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
