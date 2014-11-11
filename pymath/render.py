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
    exp = [ 2, 3, op.add, 4, op.mul]
    print(exp)
    print("txt(exp) :" + str(txt(exp)))
    print("tex(exp) :" + str(tex(exp)))
    print("p2i(exp) :" + str(p2i(exp)))
    



    
# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
