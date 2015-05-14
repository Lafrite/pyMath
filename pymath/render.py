#!/usr/bin/env python
# encoding: utf-8

from .generic import Stack,isOperator

__all__ = ['txt', 'tex', 'p2i']

class Render(object):
    """ Create functions which know how to render postfix tokens lists """

    def __init__(self, render):
        """Initiate the render
        
        :param render: function which take an operator and return a function to render the operator with his operands
        """
        self.render = render


    def __call__(self, postfix_tokens):
        """Make the object acting like a function

        :param postfix_tokens: the list of postfix tokens to be render
        :returns: the render string

        """
        operandeStack = Stack()
        for token in postfix_tokens:
            
            if isOperator(token):
                if token.arity == 1:
                    
                    op1 = operandeStack.pop()
                    
                    operandeStack.push(self.render(token)(op1))
                elif token.arity == 2:
                    op1 = operandeStack.pop()
                    op2 = operandeStack.pop()
                    # Switch op1 and op2 to respect order
                    operandeStack.push(self.render(token)(op2, op1))
            else:
                operandeStack.push(self.render(token)())

        if len(operandeStack) > 1:
            raise ValueError("This postfix_tokens is not a valid expression")
        else:
            return operandeStack.pop()

def txt_render(token):
    def render(*args):
        try:
            return getattr(token, '__txt__')(*args)
        except AttributeError:
            return str(token)
    return render

txt = Render(txt_render)
def tex_render(token):
    def render(*args):
        try:
            return getattr(token, '__tex__')(*args)
        except AttributeError:
            return str(token)
    return render
tex = Render(tex_render)

def p2i_render(token):
    def render(*args):
        try:
            return getattr(token, '__p2i__')(*args)
        except AttributeError:
            return token
    return render
p2i = Render(p2i_render)

if __name__ == '__main__':
    from .operator import op
    from itertools import permutations
    from pymath import Polynom
    from pymath import Expression 
    from pymath import Fraction
    coefs_p = [[(i-2),(j-2)] for i,j in permutations(range(5),2)] 
    coefs_q = [[2*(i-2),2*(j-2)] for i,j in permutations(range(5),2)] 
    l_p = [Polynom(i) for i in coefs_p]
    l_q = [Fraction(i,j) for i,j in coefs_q if j!=0]
    operations = [Expression([l_p[i],l_q[j],op.mul]) for i,j in permutations(range(len(l_q)),2)]
    for i in operations:
        print(i)
    



    
# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
