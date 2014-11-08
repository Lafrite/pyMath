#!/usr/bin/env python
# encoding: utf-8


from .fraction import Fraction

class Operator(str):

    """The operator class, is a string (representation of the operator) with its arity"""

    PRIORITY = {"^": 5, "/": 4, "*" : 3, ":": 3, "+": 2, "-":2, "(": 1}
    OPERATIONS = { \
            "+": ["", "", ("__add__","__radd__")],\
            "-": ["", "__neg__", ("__sub__", "__rsub__")], \
            "*": ["", "", ("__mul__", "__rmul__")], \
            "/": ["", "", ("__div__","__rdiv__")], \
            "^": ["", "", ("__pow__", "")] \
            }

    def __new__(cls, operator,  arity = 2):
        op = str.__new__(cls, operator)
        op.arity = arity

        # TODO: Add op.visibility |sam. nov.  8 17:00:08 CET 2014

        op.priority = cls.PRIORITY[operator]
        op.actions = cls.OPERATIONS[operator][arity]

        return op

    def __call__(self, *args):
        """ Calling this operator performs the rigth calculus """
        if self.arity == 1:
            return getattr(args[0], self.actions)()

        elif self.arity == 2:
            # C'est moche mais je veux que ça marche...
            if str(self) == "/":
                ans = [Fraction(args[0], args[1])]
                ans += ans[0].simplify()
                return ans
            else:
                if type(args[1]) == int:
                    return getattr(args[0], self.actions[0])(args[1])
                else:
                    return getattr(args[1], self.actions[1])(args[0])






# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
