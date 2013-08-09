#!/usr/bin/env python
# encoding: utf-8


class Expression(object):
    """A calculus expression. Today it can andle only expression with numbers later it will be able to manipulate unknown"""

    def __init__(self, exp):
        """ Initiate the expression.

        :param exp: the expression. It can be a string or a list of tokens. It can be infix or postfix expression
        """
        self._tokens = {}
        self._strings = {}
        if type(exp) == list:
            fix = self.get_fix(exp)
            self._tokens[fix] = exp
        elif type(exp) == str:
            tokens = self.parseExp(exp)
            fix = self.get_fix(tokens)
            self._tokens[fix] = tokens
            self._strings[fix] = exp
        else:
            raise ValueError("The expression needs to be a string or a list of token")

    # ---------------------
    # String parsing

    # @classmethod ????
    def parseExp(self, exp):
        """ Parse the expression, ie tranform a string into a list of tokens

        :param exp: The expression (a string)
        :returns: list of token

        """
        return exp.split(" ")

    # ---------------------
    # "fix" recognition

    def get_fix(self, tokens):
        """ Give the "fix" of an expression
        infix -> A + B
        prefix -> + A B
        postfix -> A B +

        :param exp: the expression (list of token)
        :returns: the "fix" (infix, postfix, prefix)

        """
        if tokens[0] in  "+-*/":
            return "prefix"
        elif token[0] not in "+-*/" ans token[1] not in "+-*/":
            return "postfix"
        else:
            return "infix"

    # ----------------------
    # Expressions - tokens getters

    def tokens(self, fix = "infix"):
        """Get the list of tokens with the wanted fix

        :param fix: the fix wanted (infix default)
        :returns: list of tokens

        """
        if fix not in self._tokens:
            fix_transfo = "to" + fix.capitalize()
            getattr(self,fix_transfo)()

        return self._tokens[fix]

##### On en est là,il faudra faire attention à bien vérifier ce que les "to..." enregistre (string ou tokens)  

    def string(self, fix = "infix"):
        """Get the string with the wanted fix

        :param fix: the fix wanted (infix default)
        :returns: the string representing the expression

        """
        if fix in self._string:
            return self._string[fix]
        else:
            pass
    
    # ----------------------
    # "fix" tranformations

    def toPostfix(self):
        """ Transorm the expression into postfix form """
        pass

    def toInfix(self):
        """ Tranform the expression into infix form"""
        pass

    # ---------------------
    # Tools for placing parenthesis in infix notation


    def needPar(operande, operator, posi = "after"):
        """ Says whether or not the operande needs parenthesis

        :param operande: the operande
        :param operator: the operator
        :param posi: "after"(default) if the operande will be after the operator, "before" othewise
        :returns: bollean
        """
        pass
    
    def get_main_op(exp):
        """ Gives the main operation of the expression

        :param exp: the expression
        :returns: the main operation (+, -, * or /) or 0 if the expression is only one element

        """
        pass

    # ---------------------
    # Computing the expression

    def compute(self):
        """ Recursive method for computing as a student the expression
        :returns: list of steps needed to reach the result

        """
        pass
    
    def doMath(op, op1, op2):
        """Compute "op1 op op2"

        :param op: operator
        :param op1: first operande
        :param op2: second operande
        :returns: string representing the result

        """
        return str(eval(op1 + op + op2))

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
