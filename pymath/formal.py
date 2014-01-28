#!/usr/bin/env python
# encoding: utf-8

from .fraction import Fraction
from .generic import add_in_dict, remove_in_dict, convolution_dict
import re

class FormalExp(object):
    """A formal expression (similare to Symbol in Sympy"""

    def __init__(self, coef = {}, letter = ""):
        """Initiat the formal expression

        :param coef: the dictionary representing the expression
        :param letter:  minimum expression, a letter 

        """

        if coef != {} and letter != "":
            raise ValueError("A FormalExp can't be initiate with dict_exp and a letter")
        elif letter != "":
            self._letter = letter
            self._coef = {letter: 1}
        elif coef != {}:
            self._coef = coef
        else:
            raise ValueError("FormalExp needs a letter or dictionary of coeficients")

        if len(self) != 1:
            self.mainOp = "+"

    def master_coef(self):
        """Return the master coefficient
        /!\ may not work pretty well if there is more than one indeterminate
        :returns: a_n

        """
        pattern = "\w\^(\d*)"
        finder = re.compile(pattern)
        power = {}
        for (k,v) in self._coef.items():
            if k=="":
                power[0] = v
            else:
                p = finder.findall(k)
                if p == []:
                    power[1] = v
                else:
                    power[int(p[0])] =  v

        m_power = max(power)
        return power[m_power]

    def check_calculous(self, other):
        """Check if other is a constant and then transform it into a dictionary compatible with FormalExp

        :param other: The thing to compute with the expression
        :returns: dictionary of this thing

        """
        if type(other) in [int, Fraction]:
            return {"":other}
        elif type(other) == FormalExp:
            return other._coef.copy()
        else:
            raise ValueError("Can't add {type} with FormalExp".format(type=type(other)))

    def const_or_formal(self, d):
        """Return a constant if there is nothing else, FormalExp otherwise

        :param d: dictionary descripting the expression
        :returns: a constant or a FormalExp

        """
        if list(d.keys()) == ['']:
            return d['']
        else:
            return FormalExp(d)

    def __add__(self, other):
        d = self.check_calculous(other)

        d = add_in_dict(self._coef, d)
        d = remove_in_dict(d)

        return [self.const_or_formal(d)]

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        o_tmp = -other
        return self + o_tmp

    def __neg__(self):
        d = {}
        for k,v in self._coef.items():
            d[k] = -v
        return FormalExp(d)    

    def __mul__(self, other):
        d = self.check_calculous(other)

        d = convolution_dict(self._coef, d, op_key = self.op_key)
        d = remove_in_dict(d)

        return [self.const_or_formal(d)]

    def op_key(self, x,y):
        """Operation on keys for convolution_dict"""
        if x == "" or y == "":
            return x+y
        else:
            return x + "*" + y

    
    def __rmul__(self, other):
        d = self.check_calculous(other)

        d = convolution_dict(d, self._coef, op_key = self.op_key)
        d = remove_in_dict(d)

        return [self.const_or_formal(d)]

    def __div__(self, other):
        # Will never be done :D
        pass
    
    def __pow__(self, other):
        # Will never be done :D quoique
        pass

    def __len__(self):
        return len(list(self._coef.keys()))

    def __str__(self):
        ans = ""
        for k,v in self._coef.items():
            if v < 0:
                ans += "-"
            else:
                ans += "+"

            if abs(v) == 1:
                ans += str(k)
            else:
                ans += str(abs(v)) + str(k)
        if ans[0] == "+":
            return ans[1:]
        else:
            return ans

if __name__ == '__main__':
    fe1 = FormalExp({"x": -1, "":-2})    
    print(fe1)
    fe2 = FormalExp({"x^12": 5, "":2})    
    print(fe2)
    fe3 = fe1 * fe2
    for s in fe3:
        print(s)
    fe4 = fe1 * 2
    for s in fe4:
        print(s)

    fe = FormalExp(letter = "a")
    fe_ = -2 * fe
    print(fe_[0])

    fe = FormalExp(letter = "a")
    fe_ = fe * (-2)
    print(fe_[0])




# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
