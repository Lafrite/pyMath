#!/usr/bin/env python
# encoding: utf-8


from .generic import flatten_list, isNumber
import types

class Operator(str):

    """The operator class, is a string (representation of the operator) with its arity"""

    def __new__(cls, operator = "", name = "", priority = 0, actions = ("",""), txt = "", tex = "", arity = 2):
        """ Create an Operator """
        #def __new__(cls, operator,  arity = 2):
        op = str.__new__(cls, operator)
        op.operator = operator
        op.name = name
        op.arity = arity
        op.priority = priority
        op.actions = actions
        op.txt = txt
        op.tex = tex

        op.isOperator = 1
        # TODO: Add self.visibility |sam. nov.  8 17:00:08 CET 2014
        return op

    def __call__(self, *args):
        """ Calling this operator performs the rigth calculus """
        return self._call(*args)


    def _call(self, *args):
        """Trick to avoid overloading __call__ """
        if self.arity == 1:
            return getattr(args[0], self.actions)()

        elif self.arity == 2:
            if type(args[1]) == int:
                return getattr(args[0], self.actions[0])(args[1])
            else:
                return getattr(args[1], self.actions[1])(args[0])

    def _render(self, link, *args):
        """Global step for __txt__ and __tex__

        :param link: the link between operators
        :param *args: the operands
        :returns: the string with operator and operands

        """
        if self.arity == 1:
            op1 = self.l_parenthesis(args[0], True)
            ans = link.format(op1 = op1)

        elif self.arity == 2:
            op1 = self.l_parenthesis(args[0], True)
            op2 = self.r_parenthesis(args[1], True)
            ans = link.format(op1 = op1, op2 = op2)

        ans = save_mainOp(ans, self)
        return ans

    def __txt__(self, *args):
        """Txt rendering for the operator
        
        :*args: Operands for this operation
        :returns: String with operator and his operands

        >>> op.mul.__txt__('1','2')
        '1 * 2'
        >>> op.add.__txt__('1','2')
        '1 + 2'
        >>> f = save_mainOp('2 + 3',op.add)
        >>> op.mul.__txt__(f, '4')
        '( 2 + 3 ) * 4'
        >>> f = save_mainOp('-3',op.sub1)
        >>> op.sub1.__txt__(f)
        '- ( -3 )'
        >>> op.sub1.__txt__('-3')
        '- ( -3 )'
        >>> f = save_mainOp('2 + 3',op.add)
        >>> op.sub1.__txt__(f)
        '- ( 2 + 3 )'
        """
        return self._render(self.txt, *args)

    def __tex__(self, *args):
        """Tex rendering for the operator
        
        :*args: Operands for this operation
        :returns: String with operator and his operands

        >>> op.mul.__tex__('1','2')
        '1 \\\\times 2'
        >>> op.add.__tex__('1','2')
        '1 + 2'
        >>> f = save_mainOp('2 + 3',op.add)
        >>> op.mul.__tex__(f, '4')
        '( 2 + 3 ) \\\\times 4'
        >>> f = save_mainOp('-3',op.sub1)
        >>> op.sub1.__tex__(f)
        '- ( -3 )'
        >>> op.sub1.__tex__('-3')
        '- ( -3 )'
        >>> f = save_mainOp('2 + 3',op.add)
        >>> op.sub1.__tex__(f)
        '- ( 2 + 3 )'
        """
        return self._render(self.tex, *args)

    def __p2i__(self, *args):
        """Fix list transformation for the operator
        
        :*args: Operands for this operation
        :returns: list with the operator surrounded by operands

        # TODO: order doctest  |lun. nov. 24 07:17:29 CET 2014
        >>> op.mul.__p2i__(1,2)
        [1, '*', 2]
        >>> f = save_mainOp([2, op.add, 3],op.add)
        >>> op.mul.__p2i__(f, 4)
        ['(', 2, '+', 3, ')', '*', 4]
        >>> f = save_mainOp([op.sub1, 3],op.sub1)
        >>> op.sub1.__p2i__(f)
        ['-', '(', '-', 3, ')']
        >>> op.sub1.__p2i__(-3)
        ['-', '(', -3, ')']
        >>> f = save_mainOp([2, op.add, 3],op.add)
        >>> op.sub1.__p2i__(f)
        ['-', '(', 2, '+', 3, ')']
        """
        # TODO: Attention à gestion des fractions qui se comportent chelou avec les parenthèses |dim. nov.  9 09:21:52 CET 2014
        if self.arity == 1:
            # TODO: Marche juste avec -, il faudra voir quand il y aura d'autres operateurs unitaires |dim. nov.  9 09:24:53 CET 2014
            op1 = self.l_parenthesis(args[0])
            ans = flatten_list([self, op1])

        elif self.arity == 2:
            op1 = self.l_parenthesis(args[0])
            op2 = self.r_parenthesis(args[1])
            ans = flatten_list([op1, self, op2])
        
        ans = save_mainOp(ans, self)
        return ans

    def l_parenthesis(self, opl, str_join=False):
        """ Add parenthesis for left operand if necessary """
        ans = opl
        try:
            if opl.mainOp == op.sub1:
                ans = opl
            elif opl.mainOp.priority < self.priority:
                ans = flatten_list(["(", opl, ")"])
        except AttributeError as e:
            # op has not the attribute priority
            pass

        ans = flatten_list([ans])
        if str_join:
            ans = ' '.join([str(i) for i in ans])
        return ans

    def r_parenthesis(self, op, str_join=False):
        """ Add parenthesis for left operand if necessary """
        # TODO: /!\ Parenthèses pour -2abc et l'opérateur * |lun. mars  9 19:02:32 CET 2015
        try:
            if op.mainOp.priority < self.priority:
                op = flatten_list(["(", op, ")"])
        except AttributeError:
            # op has not the attribute priority
            try:
                if int(op) < 0:
                    op = ['(', op, ')']
            except ValueError:
                pass
        ans = flatten_list([op])
        if str_join:
            ans = ' '.join([str(i) for i in ans])
        return ans

def save_mainOp(obj, mainOp):
    """Create a temporary class build over built-in type to stock the main operation of a calculus
    
    :obj: the object to add the attribute
    :mainOp: the main operator
    :returns: the same object with the main operation attribute
    """
    Fake = type('fake_'+str(type(obj)), (type(obj),), {'mainOp': mainOp})

    return Fake(obj)

def operatorize(fun):
    """Transform the answer of the function into an operator

    The returned value of the function has to be a dictionnary with those keys
        * "operator": the name (Needed!)
        * "priority": the priority level
        * "actions": mathematics actions of the operator (list of 1 element if the arity is 1, 2 elements if arity is 2)
        * "txt": string ready to be formated in txt for with {op1} and/or {op2}
        * "tex": string ready to be formated in tex for with {op1} and/or {op2}
        * "arity": arity ie number of operands needed
        * "_call": action to perform when call the operator
        * "_render": action use in __txt__ and __tex__
        * "__txt__": txt rendering
        * "__tex__": tex rendering
        * "l_parenthesis": mechanism to add parenthesis for left operande
        * "r_parenthesis": mechanism to add parenthesis for rigth operande
    """
    def mod_fun(self, *args):
        ans = fun(self, *args)

        new_op = Operator(ans["operator"])
        for (attr, value) in ans.items():
            if hasattr(value, '__call__'):
                setattr(new_op, attr, types.MethodType(value, new_op))
            else:
                setattr(new_op, attr, value)

        return new_op
    return mod_fun

class ClassProperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class op(object):
    """ List of admited operations """

    _operators = {("+",2): "add",\
            ("-", 2): "sub",\
            ("-", 1): "sub1",\
            ("*", 2): "mul",\
            ("/", 2): "div",\
            ("^", 2): "pw",\
            ("(", 2): "par",\
            }

    @classmethod
    def get_op(cls, op, arity = 2):
        """Return the corresponding operator
        
        :op: symbole of the op
        :arity: the arity

        >>> op.get_op('+')
        '+'
        >>> mul = op.get_op('*')
        >>> mul.tex
        '{op1} \\\\times {op2}'
        >>> mul.txt
        '{op1} * {op2}'
        """
        try:
            return getattr(cls, cls._operators[(op, arity)])
        except KeyError:
            raise KeyError("{theOp} (arity: {arity}) is not available".format(theOp = op, arity = arity))

    @classmethod
    def can_be_operator(cls, symbole):
        """ Tell if the symbole can be an operator """
        return symbole in [i[0] for i in cls._operators]


    @ClassProperty
    @operatorize
    def add(cls):
        """ The operator +
        
        >>> add = op.add
        >>> add
        '+'
        >>> add(1, 2)
        3
        >>> add.__tex__('1','2')
        '1 + 2'
        >>> add.__txt__('1','2')
        '1 + 2'
        >>> add.__tex__('1','-2')
        '1 + (-2)'
        """
        caract = {
            "operator" : "+", \
            "name" : "add",\
            "priority" : 1, \
            "arity" : 2, \
            "actions" : ("__add__","__radd__"), \
            "txt" :  "{op1} + {op2}",\
            "tex" :  "{op1} + {op2}",\
        }

        return caract

    @ClassProperty
    @operatorize
    def sub(self):
        """ The operator -
        
        >>> sub = op.sub
        >>> sub
        '-'
        >>> sub(1, 2)
        -1
        >>> sub.__tex__('1','2')
        '1 - 2'
        >>> sub.__txt__('1','2')
        '1 - 2'
        >>> sub.__tex__('1','-2')
        '1 - (-2)'
        >>> sub.__tex__('-1','2')
        'i-1 - 2'
        """
        def l_parenthesis(self, op, str_join=False):
            return op

        def r_parenthesis(self, op, str_join=False):
            try:
                if op.mainOp.priority <= self.priority:
                    op = flatten_list(["(", op, ")"])
            except AttributeError:
                # op has not the attribute priority
                try:
                    if int(op) < 0:
                        op = ['(', op, ')']
                except ValueError:
                    pass
            ans = flatten_list([op])
            if str_join:
                ans = ' '.join([str(i) for i in ans])
            return ans

        caract = {
            "operator" : "-", \
            "name" : "sub",\
            "priority" : 2, \
            "arity" : 2, \
            "actions" : ("__sub__","__rsub__"), \
            "txt" :  "{op1} - {op2}",\
            "tex" :  "{op1} - {op2}",\
            "l_parenthesis": l_parenthesis,\
            "r_parenthesis": r_parenthesis,\
        }

        return caract

    @ClassProperty
    @operatorize
    def sub1(self):
        """ The operator -
        
        >>> sub1 = op.sub1
        >>> sub1
        '-'
        >>> sub1(1)
        -1
        >>> sub1.__tex__('1')
        '- 1'
        >>> sub1.__txt__('1')
        '- 1'
        >>> sub1.__tex__('-1')
        '- (-1)'
        """
        def l_parenthesis(self, op, str_join=False):
            """ Add parenthesis if necessary """
            try:
                if op.mainOp.priority <= self.priority:
                    op = flatten_list(["("] + [op] + [")"])
            except AttributeError:
                # op has not the attribute priority
                try:
                    if int(op) < 0:
                        op = ['(', op, ')']
                except ValueError:
                    pass

            ans = flatten_list([op])
            if str_join:
                ans = ' '.join([str(i) for i in ans])
            return ans

        caract = {
            "operator" : "-", \
            "name" : "sub1",\
            "priority" : 3, \
            "arity" : 1, \
            "actions" : "__neg__",\
            "txt" :  "- {op1}",\
            "tex" :  "- {op1}",\
            "l_parenthesis": l_parenthesis,\
        }

        return caract

    @ClassProperty
    @operatorize
    def mul(self):
        """ The operator *
        
        >>> mul = op.mul
        >>> mul
        '*'
        >>> mul(1, 2)
        2
        >>> mul.__tex__('1','2')
        '1 \\times 2'
        >>> mul.__tex__('2','a')
        '2 a'
        >>> mul.__txt__('1','2')
        '1 * 2'
        >>> mul.__txt__('2','a')
        '2 a'
        >>> mul.__txt__('a','2')
        'a * 2'
        >>> mul.__tex__('1','-2')
        '1 \\times (-2)'
        """
        # * can not be display in some cases
        def is_visible(self, op1, op2):
            """ Tells whether self has to be visible or not

            :param op1: left operande
            :param op2: rigth operande

            """
            # TODO: À finir!!! |lun. mars  9 00:03:40 CET 2015
            if type(op2) == int:
                # op2 est maintenant une chaine de caractères
                return True
            elif op2.isdecimal():
                return True
            elif op2.isalpha():
                return False
            elif (op2[0] == "(" or op2[0].isdecimal()) and not ("+" in op2):
                return True
            else:
                return False

        def _render(self, link, *args):

            op1 = self.l_parenthesis(args[0], True)
            op2 = self.r_parenthesis(args[1], True)

            if not self.is_visible(op1, op2):
                ans = "{op1} {op2}".format(op1 = op1, op2 = op2)
            else:
                ans = link.format(op1 = op1, op2 = op2)

            ans = save_mainOp(ans, self)
            return ans

        caract = {
            "operator" : "*", \
            "name" : "mul",\
            "priority" : 4, \
            "arity" : 2, \
            "actions" : ("__mul__","__rmul__"), \
            "txt" :  "{op1} * {op2}",\
            "tex" :  "{op1} \\times {op2}",\
            "visibility": 1,\
            "_render": _render,\
            "is_visible": is_visible,\
        }

        return caract

    @ClassProperty
    @operatorize
    def div(self):
        """ The operator /
        
        >>> div = op.div
        >>> div
        '/'
        >>> div(1, 2)
        < Fraction 1 / 2>
        >>> div.__tex__('1','2')
        '\\frac{ 1 }{ 2 }'
        >>> div.__tex__('1','2')
        '\\frac{ -1 }{ 2 }'
        >>> div.__txt__('1','2')
        '1 / 2'
        """
        from .fraction import Fraction
        def _call(self, op1, op2):
            if op2 == 1:
                return op1
            else:
                return Fraction(op1,op2)

        def __tex__(self, *args):
            # Pas besoin de parenthèses en plus pour \frac
            replacement = {"op"+str(i+1): op for (i,op) in enumerate(args)}
            
            ans = self.tex.format(**replacement)
            ans = save_mainOp(ans, self)
            return ans

        caract = {
            "operator" : "/", \
            "name" : "div",\
            "priority" : 5, \
            "arity" : 2, \
            "txt" :  "{op1} / {op2}",\
            "tex" : "\\frac{{ {op1} }}{{ {op2} }}",\
            "_call": _call,\
            "__tex__":__tex__,\
        }

        return caract

    @ClassProperty
    @operatorize
    def pw(self):
        """ The operator ^
        
        >>> pw = op.pw
        >>> pw
        '^'
        >>> pw(2, 3)
        8
        >>> pw.__tex__('2','3')
        '2^{  3 }'
        >>> pw.__txt__('2','3')
        '2 ^ 3'
        >>> pw.__txt__('-2','3')
        '( -2 ) ^ 3'
        """
        def _call(self, op1, op2):
            """ Calling this operator performs the rigth calculus """
            return getattr(op1, "__pow__")(op2)

        caract = {
            "operator" : "^", \
            "name" : "pw",\
            "priority" : 6, \
            "arity" : 2, \
            "actions" : ("__pow__",""), \
            "txt" :  "{op1} ^ {op2}",\
            "tex" :  "{op1}^{{  {op2} }}",\
            "_call":_call,\
        }

        return caract

    @ClassProperty
    @operatorize
    def par(self):
        """ The operator ( """
        caract = {
            "operator" : "(", \
            "name" : "par",\
            "priority" : 0, \
            "arity" : 0, \
        }
        return caract

if __name__ == '__main__':
    #print(op.add.__tex__('1','2'))
    #print(op.mul.__tex__('1','2'))
    #print(op.sub.__tex__('1','2'))
    #f = save_mainOp('2 + 3',op.add)
    #print(op.mul.__txt__(f, '4'))
    #f = save_mainOp('-3',op.sub1)
    #print(op.sub1.__txt__(f))
    #print(op.sub1.__txt__('-3'))
    #f = save_mainOp('2 + 3',op.add)
    #print(op.sub1.__txt__(f))

    #from .fraction import Fraction
    #f = Fraction(1, 2)
    #print(op.add.__txt__(f.__txt__(),'2'))
    #print(op.add.__tex__(f.__tex__(),'2'))

    #print("\t op.can_be_operator('+') :" + str(op.can_be_operator('+')))
    #print("\t op.can_be_operator('t') :" + str(op.can_be_operator('t')))

    from .render import tex
    print(tex([-2, 3, op.add ]))
    print("-----------------")
    print(tex([-2, 3, op.mul ]))
    print("-----------------")
    from .polynom import Polynom
    print(tex([Polynom([1,2,3]), 2, op.mul]))
    print("-----------------")

    #import doctest
    #doctest.testmod()





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
