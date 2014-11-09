#!/usr/bin/env python
# encoding: utf-8

from .operator import Operator
from .generic import Stack, isOperator, isNumber

def str2tokens(exp):
    """ Parse the string into tokens then turn it into postfix form
    
    >>> str2tokens('2+3*4')
    [2, 3, 4, '*', '+']
    
    >>> str2tokens('2*3+4')
    [2, 3, '*', 4, '+']
    """
    in_tokens = str2in_tokens(exp)
    post_tokens = in2post_fix(in_tokens)

    return post_tokens

def str2in_tokens(exp):
    """ Parse the expression, ie tranform a string into a list of tokens

    /!\ float are not availiable yet!

    :param exp: The expression (a string)
    :returns: list of token

    >>> str2tokens('2+3*4')
    ['2', '+', '3', '*', '4']
    >>> str2tokens('2*3+4')
    ['2', '*', '3', '+', '4']
    """
    tokens = ['']

    for character in exp:
        if character.isdigit():
            # for "big" numbers (like 2345)
            if type(tokens[-1]) == int:
                if tokens[-1] > 0:
                    tokens[-1] = tokens[-1]*10 + int(character)
                else:
                    tokens[-1] = tokens[-1]*10 - int(character)


            # Special case for "-" at the begining of an expression or before "("
            elif tokens[-1] == "-" and \
                    str(tokens[-2]) in " (+-*/:":
                tokens[-1] = - int(character)
            else:
                tokens.append(int(character))

        elif character in "+-*/:^":
            tokens.append(Operator(character))

        elif character == ")":
            tokens.append(character)

        elif character in "(":
            # If "3(", ")("
            if isNumber(tokens[-1]) \
                    or tokens[-1] == ")" :
                        #tokens.append(Operator("*"))
                tokens.append(Operator("*"))
            tokens.append(character)

        elif character == ".":
            raise ValueError("No float number please")

        elif character != " ":
            raise ValueError("{} is an unvalid character".format(character))

    return tokens[1:]



def in2post_fix(infix_tokens):
    """ From the infix_tokens list compute the corresponding postfix_tokens list
    
    @param infix_tokens: the infix list of tokens to transform into postfix form.
    @return: the corresponding postfix list of tokens.

    >>> a, s, m, d, p = Operator("+"), Operator("-"), Operator("*"), Operator("/"), Operator("^")

    >>> in2post_fix(['(', 2, '+', 5, '-', 1, ')', '/', '(', 3, '*', 4, ')'])
    [2, 5, '+', 1, '-', 3, 4, '*', '/']
    >>> in2post_fix(['-', '(', '-', 2, ')'])
    [2, '-', '-']
    >>> in2post_fix(['-', '(', '-', 2, '+', 3, '*', 4, ')'])
    [2, '-', 3, 4, '*', '+', '-']
    """
    # Stack where operator will be stocked
    opStack = Stack()
    # final postfix list of tokens
    postfix_tokens = []
    # stack with the nbr of tokens still to compute in postfix_tokens
    arity_Stack = Stack()
    arity_Stack.push(0)

    for (pos_token,token) in enumerate(infix_tokens):

        ## Pour voir ce qu'il se passe dans cette procédure
        #print(str(postfix_tokens), " | ", str(opStack), " | ", str(infix_tokens[(pos_token+1):]), " | ", str(arity_Stack))
        if token == "(":
            opStack.push(token)
            # Set next arity counter
            arity_Stack.push(0)
        elif token == ")":
            op = opStack.pop()
            while op != "(":
                postfix_tokens.append(op)
                op = opStack.pop()

            # Go back to old arity 
            arity_Stack.pop()
            # Raise the arity
            arity = arity_Stack.pop()
            arity_Stack.push(arity + 1)

        elif isOperator(token):
            while (not opStack.isEmpty()) and (opStack.peek().priority >= token.priority):
                op = opStack.pop()
                postfix_tokens.append(op)

            arity = arity_Stack.pop() 
            
            token.arity = arity + 1
            opStack.push(token)
            # print("--", token, " -> ", str(arity + 1))
            # Reset arity to 0 in case there is other operators (the real operation would be "-op.arity + 1")
            arity_Stack.push(0)
        else:
            postfix_tokens.append(token)
            arity = arity_Stack.pop()
            arity_Stack.push(arity + 1)

    while not opStack.isEmpty():
        op = opStack.pop()
        postfix_tokens.append(op)

        # # Pour voir ce qu'il se passe dans cette procédure
        # print(str(postfix_tokens), " | ", str(opStack), " | ", str(infix_tokens[(pos_token+1):]), " | ", str(arity_Stack))

    if arity_Stack.peek() != 1:
        raise ValueError("Unvalid expression. The arity Stack is ", str(arity_Stack))

    return postfix_tokens



if __name__ == '__main__':
    #a, s, m, d, p = Operator("+"), Operator("-"), Operator("*"), Operator("/"), Operator("^")
    #in_tokens = str2in_tokens("2+3*4")
    #print("\t in_tokens :" + str(in_tokens))
    #
    #print(in2post_fix(in_tokens))

    import doctest
    doctest.testmod()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
