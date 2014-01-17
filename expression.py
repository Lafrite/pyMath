#!/usr/bin/env python
# encoding: utf-8

from generic import Stack, flatten_list, expand_list
from fraction import Fraction
from render import txt_render, post2in_fix, tex_render
from formal import FormalExp
from formal import FormalExp

class Expression(object):
    """A calculus expression. Today it can andle only expression with numbers later it will be able to manipulate unknown"""

    PRIORITY = {"*" : 3, "/": 3, "+": 2, "-":2, "(": 1}

    def __init__(self, exp):
        """ Initiate the expression

        :param exp: the expression. It can be a string or a list of tokens. It can be infix or postfix expression
        """
        if type(exp) == str:
            self._exp = exp
            self.tokens = self.str2tokens(exp) # les tokens seront alors stockés dans self.tokens temporairement
        elif type(exp) == list:
            self.tokens = exp

        self._infix_tokens = None
        self._postfix_tokens = None

        self.feed_fix() # Determine le fix et range la liste dans self.[fix]_tokens

    def __str__(self):
        """Overload str as it aim to be use in console the render is txt_render"""
        return txt_render(self.postfix_tokens)

    def render(self, render = lambda  x:str(x)):
        """ Same as __str__ but accept render as argument
        :param render: function which render the list of token (postfix form) to string

        """
        # TODO: I don't like the name of this method |ven. janv. 17 12:48:14 CET 2014
        return render(self.postfix_tokens)

    ## ---------------------
    ## Mechanism functions

    def simplify(self, render = lambda x:str(x)):
        """ Generator which return steps for computing the expression

        :param render: function which render the list of token (postfix form now) to string

        """
        if not self.can_go_further():
            yield render(self.postfix_tokens) 
        else:
            self.compute_exp() 
            old_s = ''
            for s in self.steps:
                new_s = render(s)
                # Astuce pour éviter d'avoir deux fois la même étape (par exemple pour la transfo d'une division en fraction)
                if new_s != old_s:
                    old_s = new_s
                    yield new_s
            for s in self.child.simplify(render = render):
                if old_s != s:
                    yield s

    def can_go_further(self):
        """Check whether it's a last step or not. If not create self.child the next expression.
        :returns: 1 if it's not the last step, 0 otherwise
        """
        if len(self.tokens) == 1:
            return 0
        else:
            return 1

    def compute_exp(self):
        """ Create self.child with self.steps to go up to it """
        self.steps = [self.postfix_tokens]

        tokenList = self.postfix_tokens.copy()
        tmpTokenList = []

        while len(tokenList) > 2: 
            # on va chercher les motifs du genre A B + pour les calculer
            if self.isNumber(tokenList[0]) and self.isNumber(tokenList[1]) and self.isOperator(tokenList[2]):
                
                # S'il y a une opération à faire
                op1 = tokenList[0]
                op2 = tokenList[1]
                token = tokenList[2]

                res = self.doMath(token, op1, op2)

                tmpTokenList.append(res)

                # Comme on vient de faire le calcul, on peut détruire aussi les deux prochains termes
                del tokenList[0:3]
            else:
                tmpTokenList.append(tokenList[0])

                del tokenList[0]
        tmpTokenList += tokenList

        steps = expand_list(tmpTokenList)

        if len(steps[:-1]) > 0:
            self.steps += [flatten_list(s) for s in steps[:-1]]

        self.child = Expression(steps[-1])

    ## ---------------------
    ## String parsing

    ## @classmethod ????
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
                    tokens[-1] = tokens[-1]*10 + int(character)

                # Special case for "-" at the begining of an expression or before "("
                elif tokens[-1] == "-" and \
                        str(tokens[-2]) in " (":
                    tokens[-1] = - int(character)
                else:
                    tokens.append(int(character))

            elif character.isalpha():
                # If "3x", ")x" or "yx"
                if self.isNumber(tokens[-1]) \
                        or tokens[-1] == ")" \
                        or type(tokens[-1]) == FormalExp:
                    tokens.append("*")
                    tokens.append(FormalExp(letter = character))

                # Special case for "-" at the begining of an expression or before "("
                elif tokens[-1] == "-" \
                        or str(tokens[-2]) in " (":
                    tokens[-1] = - FormalExp(letter = character)

                else:
                    tokens.append(FormalExp(letter = character))

            elif character in "+-*/)":
                tokens.append(character)

            elif character in "(":
                # If "3(", ")(" or "x("
                if self.isNumber(tokens[-1]) \
                        or tokens[-1] == ")" \
                        or type(tokens[-1]) == FormalExp:
                    tokens.append("*")
                tokens.append(character)

            elif character != " ":
                raise ValueError("{} is an unvalid character".format(character))

        return tokens[1:]

    # ---------------------
    # "fix" recognition

    @classmethod
    def get_fix(self, tokens):
        """ Give the "fix" of an expression
        [A, +, B] -> infix, or if there is parenthesis it is infix
        [+, A, B] -> prefix
        [A, B, +] -> postfix
        /!\ does not verify if the expression is correct/computable!

        :param exp: the expression (list of token)
        :returns: the "fix" (infix, postfix, prefix)

        """
        if self.isOperator(tokens[0]):
            return "prefix"
        elif "(" in tokens:
            return "infix"
        elif not self.isOperator(tokens[0]) and not self.isOperator(tokens[1]):
            return "postfix"
        else:
            return "infix"

    def feed_fix(self):
        """ Recognize the fix of self.tokens and stock tokens in self.[fix]_tokens """
        if len(self.tokens) > 1:
            fix = self.get_fix(self.tokens)
        else:
            fix = "postfix" # Completement arbitraire mais on s'en fiche!

        setattr(self, fix+"_tokens", self.tokens)


    # ----------------------
    # Expressions - tokens manipulation

    @property
    def infix_tokens(self):
        """ Return infix list of tokens. Verify if it has already been computed and compute it if not

        :returns: infix list of tokens
        """
        if self._infix_tokens:
            return self._infix_tokens

        elif self._postfix_tokens:
            self._infix_tokens = post2in_fix(self._postfix_tokens)
            return self._infix_tokens

        else:
            raise ValueError("Unkown fix")

    @infix_tokens.setter
    def infix_tokens(self, val):
        self._infix_tokens = val

    @property
    def postfix_tokens(self):
        """ Return postfix list of tokens. Verify if it has already been computed and compute it if not

        :returns: postfix list of tokens
        """
        if self._postfix_tokens:
            return self._postfix_tokens

        elif self._infix_tokens:
            self._postfix_tokens = self.in2post_fix(self._infix_tokens)
            return self._postfix_tokens

        else:
            raise ValueError("Unkown fix")

    @postfix_tokens.setter
    def postfix_tokens(self, val):
        self._postfix_tokens = val

    # ----------------------
    # "fix" tranformations

    @classmethod
    def in2post_fix(cls, infix_tokens):
        """ From the infix_tokens list compute the corresponding postfix_tokens list
        
        @param infix_tokens: the infix list of tokens to transform into postfix form.
        @return: the corresponding postfix list of tokens.

        >>> Expression.in2post_fix(['(', 2, '+', 5, '-', 1, ')', '/', '(', 3, '*', 4, ')'])
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

    ## ---------------------
    ## Computing the expression

    @staticmethod
    def doMath(op, op1, op2):
        """Compute "op1 op op2" or create a fraction

        :param op: operator
        :param op1: first operande
        :param op2: second operande
        :returns: string representing the result

        """
        if op == "/":
            ans = [Fraction(op1, op2)]
            ans += ans[0].simplify()
            return ans
        else:
            if type(op2) != int:
                operations = {"+": "__radd__", "-": "__rsub__", "*": "__rmul__"}
                return getattr(op2,operations[op])(op1)
            else:
                operations = {"+": "__add__", "-": "__sub__", "*": "__mul__"}
                return getattr(op1,operations[op])(op2)


    ## ---------------------
    ## Recognize numbers and operators

    @staticmethod
    def isNumber(exp):
        """Check if the expression can be a number

        :param exp: an expression
        :returns: True if the expression can be a number and false otherwise

        """
        return type(exp) == int or \
                type(exp) == Fraction or \
                type(exp) == FormalExp

    @staticmethod
    def isOperator(exp):
        """Check if the expression is an opération in "+-*/"

        :param exp: an expression
        :returns: boolean

        """
        return (type(exp) == str and exp in "+-*/")


def test(exp):
    a = Expression(exp)
    #for i in a.simplify():
    #for i in a.simplify(render = txt_render):
    for i in a.simplify(render = tex_render):
        print(i)

    print("\n")

if __name__ == '__main__':
    #exp = "1 + 3 * 5"
    #test(exp)

    #exp = "2 * 3 * 3 * 5"
    #test(exp)

    #exp = "2 * 3 + 3 * 5"
    #test(exp)

    #exp = "2 * ( 3 + 4 ) + 3 * 5"
    #test(exp)

    #exp = "2 * ( 3 + 4 ) + ( 3 - 4 ) * 5"
    #test(exp)
    #
    #exp = "2 * ( 2 - ( 3 + 4 ) ) + ( 3 - 4 ) * 5"
    #test(exp)
    #
    #exp = "2 * ( 2 - ( 3 + 4 ) ) + 5 * ( 3 - 4 )"
    #test(exp)
    #
    #exp = "2 + 5 * ( 3 - 4 )"
    #test(exp)

    #exp = "( 2 + 5 ) * ( 3 - 4 )"
    #test(exp)

    #exp = "( 2 + 5 ) * ( 3 * 4 )"
    #test(exp)

    #exp = "( 2 + 5 - 1 ) / ( 3 * 4 )"
    #test(exp)

    #exp = "( 2 + 5 ) / ( 3 * 4 ) + 1 / 12"
    #test(exp)

    #exp = "( 2+ 5 )/( 3 * 4 ) + 1 / 2"
    #test(exp)

    #exp="(-2+5)/(3*4)+1/12+5*5"
    #test(exp)

    exp="-2*4(12 + 1)(3-12)"
    test(exp)

    exp="-2+a+(12 + 1)(3-12) + 34a"
    test(exp)
    e = Expression(exp)
    print(e)

    #exp="-2*b+a(12 + 1)(3-12)"
    #test(exp)

    # TODO: The next one doesn't work  |ven. janv. 17 14:56:58 CET 2014
    #exp="-2*(-a)(12 + 1)(3-12)"
    #e = Expression(exp)
    #print(e)

    ## Can't handle it yet!!
    #exp="-(-2)"
    #test(exp)

    import doctest
    doctest.testmod()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
