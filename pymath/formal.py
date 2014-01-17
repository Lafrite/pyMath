#!/usr/bin/env python
# encoding: utf-8

from .fraction import Fraction
from .generic import add_in_dict, remove_in_dict
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
        pattern = "\w\*\*(\d*)"
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

    def __add__(self, other):
        if type(other) in [int, Fraction]:
            d = {"":other}
        elif type(other) == FormalExp:
            d = other._coef
        else:
            raise ValueError("Can't add {type} with FormalExp".format(type=type(other)))

        d = add_in_dict(self._coef, d)
        d = remove_in_dict(d)
        if list(d.keys()) == ['']:
            return [d['']]
        else:
            return [FormalExp(d)]

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
        pass
    
    def __rmul__(self, other):
        pass

    def __div__(self, other):
        pass
    
    def __pow__(self, other):
        pass

    def __len__(self):
        return len(list(self._coef.keys()))

    def __str__(self):
        return " + ".join([str(v) + str(k) for k,v in self._coef.items()])
    
if __name__ == '__main__':
    #fe1 = FormalExp({"x": 1, "":2})    
    #print(fe1)
    #fe2 = FormalExp({"x**12": 5, "":2})    
    #print(fe2)
    #fe3 = fe1 + fe2
    #for s in fe3:
    #    print(s)
    #fe4 = fe1 + 2
    #for s in fe4:
    #    print(s)

    #print(fe1.master_coef())
    #print(fe2.master_coef())
    #print(fe3[0].master_coef())
    #print(fe4[0].master_coef())

    fe = FormalExp(letter = "a")
    fe_ = -2 + fe
    print(fe_[0])





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
