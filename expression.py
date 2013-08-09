#!/usr/bin/env python
# encoding: utf-8


class Expression(object):
    """A calculus expression. Today it can andle only expression with numbers later it will be able to manipulate unknown"""

    def __init__(self, exp):
        """ Initiate the expression.

        :param exp: the expression. It can be a string or a list of tokens. It can be infix or postfix expression
        """
        pass

    # ---------------------
    # String parsing

    # @classmethod ????
    def parseExp(self, exp):
        """ Parse the expression, ie tranform a string into a list of tokens

        :param exp: The expression
        :returns: list of token

        """
        pass

    # ---------------------
    # "fix" recognition

    def expressionFix(self, exp):
        """ Give the "fix" of an expression
        infix -> A + B
        prefix -> + A B
        postfix -> A B +

        :param exp: the expression
        :returns: the "fix" (infix, postfix, prefix)

        """
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
