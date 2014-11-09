#!/usr/bin/env python
# encoding: utf-8


from .fraction import Fraction
from .generic import flatten_list

class Operator(str):

    """The operator class, is a string (representation of the operator) with its arity"""

    PRIORITY = {"^": [0, 5], "/": [0, 4], "*" : [0,3], ":": [0,3], "+": [0,1], "-":[2,1]}
    OPERATIONS = { \
            "+": ["", ("__add__","__radd__")],\
            "-": ["__neg__", ("__sub__", "__rsub__")], \
            "*": ["", ("__mul__", "__rmul__")], \
            "/": ["", ("__div__","__rdiv__")], \
            "^": ["", ("__pow__", "")] \
            }
    TXT = { \
            "+": ["", "{op1} + {op2}"] ,\
            "-": ["- {op1}", "{op1} - {op2}"] ,\
            "*": ["", "{op1} * {op2}"] ,\
            "/": ["", "{op1} / {op2}"] ,\
            "^": ["", "{op1} ^ {op2}"] ,\
            }
    TEX = { \
            "+": ["", "{op1} + {op2}"] ,\
            "-": ["- {op1}", "{op1} - {op2}"] ,\
            "*": ["", "{op1} \\times {op2}"] ,\
            "/": ["", "\\frac{{ {op1} }}{{ {op2} }}"] ,\
            "^": ["", "{op1}^{{ {op2} }}"] ,\
            }


    def __new__(cls, operator,  arity = 2):
        op = str.__new__(cls, operator)
        op.arity = arity

        # TODO: Add op.visibility |sam. nov.  8 17:00:08 CET 2014

        op.priority = cls.PRIORITY[operator][arity - 1]
        op.actions = cls.OPERATIONS[operator][arity-1]
        op._txt = cls.TXT[operator][arity-1]
        op._tex = cls.TEX[operator][arity-1]

        op.isOperator = 1

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

    def __txt__(self, *args):
        """Txt rendering for the operator
        
        :*args: Operands for this operation
        :returns: String with operator and his operands

        >>> mul = Operator("*", 2)
        >>> add = Operator("+", 2)
        >>> sub1 = Operator("-", 1)
        >>> div = Operator("/", 1)
        >>> mul.__txt__(1,2)
        '1 * 2'
        >>> add.__txt__(1,2)
        '1 + 2'
        >>> f = save_mainOp('2 + 3',add)
        >>> mul.__txt__(f, 4)
        '( 2 + 3 ) * 4'
        >>> f = save_mainOp('-3',sub1)
        >>> sub1.__txt__(f)
        '- ( -3 )'
        >>> sub1.__txt__(-3)
        '- ( -3 )'
        >>> f = save_mainOp('2 + 3',add)
        >>> sub1.__txt__(f)
        '- ( 2 + 3 )'
        """
        
        #vive le inline? ...
        replacement = {"op"+str(i+1): ' '.join([str(o) if type(o)==int else o for o in self.add_parenthesis(op)]) for (i,op) in enumerate(args)}
        
        ans = self._txt.format(**replacement)
        ans = save_mainOp(ans, self)
        return ans

    def __tex__(self, *args):
        """Tex rendering for the operator
        
        :*args: Operands for this operation
        :returns: String with operator and his operands

        >>> mul = Operator("*", 2)
        >>> add = Operator("+", 2)
        >>> sub1 = Operator("-", 1)
        >>> div = Operator("/", 1)
        >>> mul.__tex__(1,2)
        '1 \\\\times 2'
        >>> add.__tex__(1,2)
        '1 + 2'
        >>> f = save_mainOp('2 + 3',add)
        >>> mul.__tex__(f, 4)
        '( 2 + 3 ) \\\\times 4'
        >>> f = save_mainOp('-3',sub1)
        >>> sub1.__tex__(f)
        '- ( -3 )'
        >>> sub1.__tex__(-3)
        '- ( -3 )'
        >>> f = save_mainOp('2 + 3',add)
        >>> sub1.__tex__(f)
        '- ( 2 + 3 )'
        """
        replacement = {"op"+str(i+1): ' '.join([str(o) if type(o)==int else o for o in self.add_parenthesis(op)]) for (i,op) in enumerate(args)}
        
        ans = self._tex.format(**replacement)
        ans = save_mainOp(ans, self)
        return ans

    def __p2i__(self, *args):
        """Fix list transformation for the operator
        
        :*args: Operands for this operation
        :returns: list with the operator surrounded by operands

        >>> mul = Operator("*", 2)
        >>> add = Operator("+", 2)
        >>> sub1 = Operator("-", 1)
        >>> mul.__p2i__(1,2)
        [1, '*', 2]
        >>> f = save_mainOp([2, add, 3],add)
        >>> mul.__p2i__(f, 4)
        ['(', 2, '+', 3, ')', '*', 4]
        >>> f = save_mainOp([sub1, 3],sub1)
        >>> sub1.__p2i__(f)
        ['-', '(', '-', 3, ')']
        >>> sub1.__p2i__(-3)
        ['-', '(', -3, ')']
        >>> f = save_mainOp([2, add, 3],add)
        >>> sub1.__p2i__(f)
        ['-', '(', 2, '+', 3, ')']
        """
        # TODO: Attention à gestion des fractions qui se comportent chelou avec les parenthèses |dim. nov.  9 09:21:52 CET 2014
        if self.arity == 1:
            # TODO: Marche juste avec -, il faudra voir quand il y aura d'autres operateurs unitaires |dim. nov.  9 09:24:53 CET 2014
            op1 = self.add_parenthesis(args[0])
            ans = flatten_list([self, op1])

        elif self.arity == 2:
            op1 = self.add_parenthesis(args[0])
            op2 = self.add_parenthesis(args[1])
            ans = flatten_list([op1, self, op2])
        
        ans = save_mainOp(ans, self)
        return ans

    def add_parenthesis(self, op):
        """ Add parenthesis if necessary """
        try:
            if op.mainOp.priority < self.priority:
                op = flatten_list(["("] + [op] + [")"])
        except AttributeError:
            if type(op) == int and op < 0:
                op = ['(', op, ')']
        return flatten_list([op])




def save_mainOp(obj, mainOp):
    """Create a temporary class build over built-in type to stock the main operation of a calculus
    
    :obj: the object to add the attribute
    :mainOp: the main operator
    :returns: the same object with the main operation attribute
    """
    class Fake(type(obj)):
        """ The fake class """
        def __new__(cls, obj):
            op = type(obj).__new__(cls, obj)
            op.mainOp = mainOp
            return op

    return Fake(obj)

if __name__ == '__main__':
    #op = Operator("+", 2)
    #print(op.__txt__(1,2))
    #mul = Operator("*", 2)
    #add = Operator("+", 2)
    #sub1 = Operator("-", 1)
    #div = Operator("/", 1)
    #print(mul.__txt__(1,2))
    #print(add.__txt__(1,2))
    #f = save_mainOp('2 + 3',add)
    #print(mul.__txt__(f, 4))
    #f = save_mainOp('-3',sub1)
    #print(sub1.__txt__(f))
    #print(sub1.__txt__(-3))
    #f = save_mainOp('2 + 3',add)
    #print(sub1.__txt__(f))

    import doctest
    doctest.testmod()





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
