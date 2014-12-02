#!/usr/bin/env python
# encoding: utf-8


from .generic import flatten_list, isNumber

class Operator(object):

    """The operator class, is a string (representation of the operator) with its arity"""

    def __init__(self, operator = "", priority = 0, actions = ("",""), txt = "", tex = "", arity = 2):
        """ Create an Operator """
        self.name = operator
        self.arity = arity

        # TODO: Add self.visibility |sam. nov.  8 17:00:08 CET 2014

        self.priority = priority
        self.actions = actions
        self.txt = txt
        self.tex = tex

        self.isselferator = 1

    def __str__(self):
        return self.name

    def __call__(self, *args):
        """ Calling this operator performs the rigth calculus """
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
        replacement = {"op"+str(i+1): ' '.join(self.add_parenthesis(op)) for (i,op) in enumerate(args)}
        
        ans = link.format(**replacement)
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
            # op has not the attribute priority
            try:
                if int(op) < 0:
                    op = ['(', op, ')']
            except ValueError:
                pass
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

def operatorize(fun):
    """Transform the answer of the function into an operator

    The returned value of the function has to be a dictionnary with those keys
        * "operator": the name (Needed!)
        * "priority": the priority level
        * "action": mathematic action of the operator (list of 1 element if the arity is 1, 2 elements if arity is 2)
        * "txt": string ready to be formated in txt for with {op1} and/or {op2}
        * "tex": string ready to be formated in tex for with {op1} and/or {op2}
        * "arity": arity ie number of operands needed
        * "__call__": action to perform when call the operator
        * "_render": action use in __txt__ and __tex__
        * "__txt__": txt rendering
        * "__tex__": tex rendering
        * "add_parenthesis": mechanism to add parenthesis
    """
    def mod_fun(self, *args):
        ans = fun(self, *args)

        op = Operator(ans["operator"])
        print("type(op)", type(op))
        for (attr, value) in ans.items():
            if hasattr(value, '__call__'):
                print("value :", type(value))
                print("value :", str(value))
                callback = lambda *args, **kwrds: value(op, *args, **kwrds)
                setattr(op, attr, callback)
            else:
                setattr(op, attr, value)
        return op
    return mod_fun

class ClassProperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)

class op(object):
    """ List of admited operations """

    @ClassProperty
    @operatorize
    def add(cls):
        """ The operator + """
        caract = {
            "operator" : "+", \
            "priority" : 1, \
            "arity" : 2, \
            "action" : ("__add__","__radd__"), \
            "txt" :  "{op1} + {op2}",\
            "tex" :  "{op1} + {op2}",\
        }

        return caract

    @ClassProperty
    @operatorize
    def sub(self):
        """ The operator - """
        caract = {
            "operator" : "-", \
            "priority" : 1, \
            "arity" : 2, \
            "action" : ("__sub__","__rsub__"), \
            "txt" :  "{op1} - {op2}",\
            "tex" :  "{op1} - {op2}",\
        }

        return caract

    @ClassProperty
    @operatorize
    def sub1(self):
        """ The operator - """
        def add_parenthesis(self, op):
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
            return flatten_list([op])

        caract = {
            "operator" : "-", \
            "priority" : 2, \
            "arity" : 2, \
            "action" : "__neg__",\
            "txt" :  "- {op1}",\
            "tex" :  "- {op1}",\
            "add_parenthesis": add_parenthesis,\
        }

        return caract

    @ClassProperty
    @operatorize
    def mul(self):
        """ The operator * """
        # * can not be display in some cases
        def _render(self, link, *args):

            #print("self->", str(self))
            #print("link ->", str(link))
            #print("*args ->", str(args))

            replacement = {"op"+str(i+1): ' '.join(self.add_parenthesis(op)) for (i,op) in enumerate(args)}

            if not self.visibility or args[1][0] == "(" or \
                    (type(args[1][0]) == str and args[1][0].isalpha()):
                ans = "{op1} {op2}".format(**replacement)
                ans = save_mainOp(ans, self)
                return ans
            else:
                ans = link.format(**replacement)
                ans = save_mainOp(ans, self)
                return ans

        caract = {
            "operator" : "*", \
            "priority" : 4, \
            "arity" : 2, \
            "action" : ("__mul__","__rmul__"), \
            "txt" :  "{op1} * {op2}",\
            "tex" :  "{op1} \\times {op2}",\
            "visibility": 1,\
            "_render": _render
        }

        return caract

    @ClassProperty
    @operatorize
    def div(self):
        """ The operator / """
        def __call__(self, op1, op2):
            if op2 == 1:
                return op1
            else:
                return Fraction(op1,op2)

        def __tex__(self, *args):
            # Pas besoin de parenthèses en plus pour \frac
            replacement = {"op"+str(i+1): op for (i,op) in enumerate(args)}
            
            ans = self._tex.format(**replacement)
            ans = save_mainOp(ans, self)
            return ans

        caract = {
            "operator" : "/", \
            "priority" : 4, \
            "arity" : 2, \
            "txt" :  "{op1} /^ {op2}",\
            "tex" : "\\frac{{ {op1} }}{{ {op2} }}",\
            "__call__": __call__,\
            "__tex__":__tex__,\
        }

        return caract

    @ClassProperty
    @operatorize
    def pw(self):
        """ The operator ^ """
        caract = {
            "operator" : "^", \
            "priority" : 5, \
            "arity" : 2, \
            "action" : ("__pow__",""), \
            "txt" :  "{op1} ^ {op2}",\
            "tex" :  "{op1}^{{  {op2} }}",\
        }

        return caract

    @ClassProperty
    @operatorize
    def par(self):
        """ The operator ( """
        caract = {
            "operator" : "(", \
            "priority" : 0, \
            "arity" : 0, \
        }
        return caract

if __name__ == '__main__':
    print(op.add.__txt__('1','2'))
    print(op.mul.__txt__('1','2'))
    print(op.sub.__txt__('1','2'))
    f = save_mainOp('2 + 3',op.add)
    print(op.mul.__txt__(f, '4'))
    f = save_mainOp('-3',op.sub1)
    print(op.sub1.__txt__(f))
    print(op.sub1.__txt__('-3'))
    f = save_mainOp('2 + 3',op.add)
    print(op.sub1.__txt__(f))

    from .fraction import Fraction
    f = Fraction(1, 2)
    print(op.add.__txt__(f.__txt__(),'2'))
    print(op.add.__tex__(f.__tex__(),'2'))
    

    import doctest
    doctest.testmod()





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
