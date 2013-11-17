#!/usr/bin/env python
# encoding: utf-8

from generic import Stack


def post2in_fix(postfix_tokens):
    """ From the postfix_tokens list compute the corresponding infix_tokens list
    
    @param postfix_tokens: the postfix list of tokens to transform into infix form. If nothing is set, it takes the value self.postfix_tokens
    @return: the corresponding infix list of tokens if postfix_tokens is set. nothing otherwise but stock it in self.infix_tokens

    >>> post2in_fix([2, 5, '+', 1, '-', 3, 4, '*', '/'])
    ['( ', 2, '+', 5, '-', 1, ' )', '/', '( ', 3, '*', 4, ' )']
    """
    operandeStack = Stack()

    for token in postfix_tokens:
        if self.isOperator(token):
            op2 = operandeStack.pop()
            if self.needPar(op2, token, "after"):
                op2 = ["( ", op2, " )"]
            op1 = operandeStack.pop()
            if self.needPar(op1, token, "before"):
                op1 = ["( ", op1, " )"]
            res = [op1, token, op2]

            operandeStack.push(res)

        else:
            operandeStack.push(token)

    infix_tokens = flatten_list(operandeStack.pop())

    return infix_tokens

def textRender(postfix_tokens):
    """ A text baser render

    :param postfix_tokens: The postfix list of tokens
    :returns: the text expression

    """
    infix_tokens = post2in_fix(postfix_tokens)
    return ' '.join(infix_tokens)

if __name__ == '__main__':
    
    import doctest
    doctest.testmod()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
