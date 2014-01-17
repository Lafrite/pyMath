#!/usr/bin/env python
# encoding: utf-8

from .generic import Stack,flatten_list
from .fraction import Fraction
from .formal import FormalExp

        
class Render(object):
    """A class which aims to create render functions from three dictionnaries:
        - op_infix: dict of caracters
        - op_postfix: dict of 2 arguments functions
        - other: dict of caracters
    Those three dictionnaries while define how a postfix expression will be transform into a string.
    """

    PRIORITY = {"^": 4,"*" : 3, "/": 3, ":": 3, "+": 2, "-":2, "(": 1}

    def __init__(self, op_infix = {}, op_postfix = {}, other = {}, join = " ", type_render = {int: str, Fraction: str, FormalExp: str}):
        """Initiate the render
        
        @param op_infix: the dictionnary of infix operator with how they have to be render
        @param op_postfix: the dictionnary of postfix operator with how they have to be render
        @param other: other caracters like parenthesis.
        @param raw: the caracter for joining the list of tokens (if False then it returns the list of tokens)
        @param type_render: how to render number (str or tex for fractions for example)
        """

        self.op_infix = op_infix
        self.op_postfix = op_postfix
        self.other = other
        # TODO: there may be issues with PRIORITY if a sign does not appear in PRIORITY

        self.join = join
        self.type_render = type_render

        self.operators = list(self.op_infix.keys()) + list(self.op_postfix.keys()) + list(self.other.keys())

    def __call__(self, postfix_tokens):
        """Make the object acting like a function

        :param postfix_tokens: the list of postfix tokens to be render
        :returns: the render string

        """
        operandeStack = Stack()

        
        for token in postfix_tokens:
            if self.isOperator(token):

                op2 = operandeStack.pop()
                if self.needPar(op2, token, "after"):
                    op2 = [self.other["("] ,  op2 , self.other[")"]]

                op1 = operandeStack.pop()
                if self.needPar(op1, token, "before"):
                    op1 = [self.other["("] ,  op1 , self.other[")"]]

                if token in self.op_infix:
                    res = flist([op1 , self.op_infix[token] ,  op2])

                elif token in self.op_postfix:
                    res = flist([self.op_postfix[token](op1, op2)])

                # Trick to remember the main op when the render will be done!
                res.mainOp = token

                operandeStack.push(res)

            else:
                operandeStack.push(token)

            
        # Manip pour gerer les cas de listes imbriquées dans d'autres listes
        infix_tokens = operandeStack.pop()
        if type(infix_tokens) == list or type(infix_tokens) == flist:
            infix_tokens = flatten_list(infix_tokens)
        elif self.isNumerande(infix_tokens):
            infix_tokens = [infix_tokens]

        if self.join:
            return self.join.join(flatten_list([self.render_from_type(t) for t in infix_tokens]))
        else:
            return infix_tokens

    def render_from_type(self, op):
        """ If the op is a numerande, it transforms it with type_render conditions

        :param op: the operator
        :returns: the op transformed if it's necessary

        """
        if self.isNumerande(op):
            return self.type_render[type(op)](op)
        else:
            return op


    # ---------------------
    # Tools for placing parenthesis in infix notation

    def needPar(self, operande, operator, posi = "after"):
        """Says whether or not the operande needs parenthesis

        :param operande: the operande
        :param operator: the operator
        :param posi: "after"(default) if the operande will be after the operator, "before" othewise
        :returns: bollean
        """
        # Si l'operande est negatif
        if self.isNumber(operande) \
                and operande < 0:
            return 1
            
        # Si c'est un expression formelle
        elif type(operande) == FormalExp:
            if operator in ["*", "/", "^"]:
                if len(operande) > 1 \
                        or operande.master_coef() < 0:
                    return 1
            else:
                return 0

        elif not self.isNumber(operande):
            # Si c'est une grande expression ou un chiffre négatif
            stand_alone = self.get_main_op(operande)
            # Si la priorité de l'operande est plus faible que celle de l'opérateur
            minor_priority = self.PRIORITY[self.get_main_op(operande)] < self.PRIORITY[operator]
            # Si l'opérateur est - ou / pour after ou / ou ^ pour before
            special = (operator in "-/" and posi == "after") or (operator in "/^" and posi == "before")

            return stand_alone and (minor_priority or special)
        else:
            return 0

    def get_main_op(self, tokens):
        """Getting the main operation of the list of tokens

        :param exp: the list of tokens
        :returns: the main operation (+, -, * or /) or 0 if the expression is only one element

        """
        if hasattr(tokens, "mainOp"):
            return tokens.mainOp

        if len(tokens) == 1:
            # Si l'expression n'est qu'un élément
            return 0

        parStack = Stack()
        main_op = []

        for token in tokens:
            if token == "(":
                parStack.push(token)
            elif token == ")":
                parStack.pop()
            elif self.isOperator(token) and parStack.isEmpty():
                main_op.append(token)

        return min(main_op, key = lambda s: self.PRIORITY[s])

    ## ---------------------
    ## Recognize numbers and operators

    @staticmethod
    def isNumber( exp):
        """Check if the expression can be a number which means int or Fraction

        :param exp: an expression
        :returns: True if the expression can be a number and false otherwise

        """
        return type(exp) == int \
                or type(exp) == Fraction
        #return type(exp) == int or type(exp) == Fraction

    @staticmethod
    def isNumerande(exp):
        """Check if the expression can be a numerande (not an operator)

        :param exp: an expression
        :returns: True if the expression can be a number and false otherwise

        """
        return type(exp) == int \
                or type(exp) == Fraction \
                or type(exp) == FormalExp

    def isOperator(self, exp):
        """Check if the expression is in self.operators

        :param exp: an expression
        :returns: boolean

        """
        return (type(exp) == str and exp in self.operators)
        
class flist(list):
    """Fake list- they are used to stock the main operation of an rendered expression"""
    pass


    
# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
