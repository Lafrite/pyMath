#!/usr/bin/env python
# encoding: utf-8



def str2tokens(self, exp):
    """ Parse the expression, ie tranform a string into a list of tokens

    /!\ float are not availiable yet!

    :param exp: The expression (a string)
    :returns: list of token

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

        elif character in "+-*/):^":
            tokens.append(character)

        elif character in "(":
            # If "3(", ")("
            if self.isNumber(tokens[-1]) \
                    or tokens[-1] == ")" :
                tokens.append("*")
            tokens.append(character)

        elif character == ".":
            raise ValueError("No float number please")

        elif character != " ":
            raise ValueError("{} is an unvalid character".format(character))

    return tokens[1:]



def in2post_fix(cls, infix_tokens):
    """ From the infix_tokens list compute the corresponding postfix_tokens list
    
    @param infix_tokens: the infix list of tokens to transform into postfix form.
    @return: the corresponding postfix list of tokens.

    >>> .in2post_fix(['(', 2, '+', 5, '-', 1, ')', '/', '(', 3, '*', 4, ')'])
    [2, 5, '+', 1, '-', 3, 4, '*', '/']
    """
    opStack = Stack()
    postfixList = []

    for token in infix_tokens:
        if token == "(":
            opStack.push(token)
        elif token == ")":
            topToken = opStack.pop()
            while topToken != "(":
                postfixList.append(topToken)
                topToken = opStack.pop()
        elif cls.isOperator(token):
            # On doit ajouter la condition == str sinon python ne veut pas tester l'appartenance à la chaine de caractère. 
            while (not opStack.isEmpty()) and (cls.PRIORITY[opStack.peek()] >= cls.PRIORITY[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)
        else:
            postfixList.append(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())

    return postfixList





# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
