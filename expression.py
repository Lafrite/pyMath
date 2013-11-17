#!/usr/bin/env python
# encoding: utf-8

from generic import Stack, flatten_list, expand_list
from fraction import Fraction

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

    ## ---------------------
    ## Mechanism functions

    def simplify(self, render = lambda x:str(x)):
        """ Generator which return steps for computing the expression

        @param render: function which render the list of token (postfix form now)

        """
        print("\t ---------- In simplify ---------- ")
        
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

        :param exp: The expression (a string)
        :returns: list of token

        """
        tokens = exp.split(" ")

        for (i,t) in enumerate(tokens):
            try:
                tokens[i] = int(t)
            except ValueError:
                pass

        return tokens

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
            self._infix_tokens = self.post2in_fix(self._postfix_tokens)
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
    def in2post_fix(self, infix_tokens):
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
            elif self.isOperator(token):
                # On doit ajouter la condition == str sinon python ne veut pas tester l'appartenance à la chaine de caractère. 
                while (not opStack.isEmpty()) and (self.PRIORITY[opStack.peek()] >= self.PRIORITY[token]):
                    postfixList.append(opStack.pop())
                opStack.push(token)
            else:
                postfixList.append(token)

        while not opStack.isEmpty():
            postfixList.append(opStack.pop())

        return postfixList

    @classmethod
    def post2in_fix(self, postfix_tokens):
        """ From the postfix_tokens list compute the corresponding infix_tokens list
        
        @param postfix_tokens: the postfix list of tokens to transform into infix form.
        @return: the corresponding infix list of tokens if postfix_tokens.

        >>> Expression.post2in_fix([2, 5, '+', 1, '-', 3, 4, '*', '/'])
        ['( ', 2, '+', 5, '-', 1, ' )', '/', '( ', 3, '*', 4, ' )']
        >>> Expression.post2in_fix([2])
        [2]
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
            
        # Manip pour gerer les cas similaires au deuxième exemple
        infix_tokens = operandeStack.pop()
        if type(infix_tokens) == list:
            infix_tokens = flatten_list(infix_tokens)
        elif self.isNumber(infix_tokens):
            infix_tokens = [infix_tokens]

        return infix_tokens

    # ---------------------
    # Tools for placing parenthesis in infix notation

    @classmethod
    def needPar(self, operande, operator, posi = "after"):
        """Says whether or not the operande needs parenthesis

        :param operande: the operande
        :param operator: the operator
        :param posi: "after"(default) if the operande will be after the operator, "before" othewise
        :returns: bollean
        """
        if self.isNumber(operande) and operande < 0:
            return 1
        elif not self.isNumber(operande):
            # Si c'est une grande expression ou un chiffre négatif
            stand_alone = self.get_main_op(operande)
            # Si la priorité de l'operande est plus faible que celle de l'opérateur
            minor_priority = self.PRIORITY[self.get_main_op(operande)] < self.PRIORITY[operator]
            # Si l'opérateur est -/ pour after ou juste / pour before
            special = (operator in "-/" and posi == "after") or (operator in "/" and posi == "before")

            return stand_alone and (minor_priority or special)
        else:
            return 0
    
    @classmethod
    def get_main_op(self, tokens):
        """Getting the main operation of the list of tokens

        :param exp: the list of tokens
        :returns: the main operation (+, -, * or /) or 0 if the expression is only one element

        """
        parStack = Stack()

        if len(tokens) == 1:
        # Si l'expression n'est qu'un élément
            return 0

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
    ## Computing the expression

    @staticmethod
    def doMath(op, op1, op2):
        """Compute "op1 op op2" or create a fraction

        :param op: operator
        :param op1: first operande
        :param op2: second operande
        :returns: string representing the result

        """
        operations = {"+": "__add__", "-": "__sub__", "*": "__mul__"}
        if op == "/":
            ans = [Fraction(op1, op2)]
            ans += ans[0].simplify()
            return ans
        else:
            return getattr(op1,operations[op])(op2)

    ## ---------------------
    ## Recognize numbers and operators

    @staticmethod
    def isNumber(exp):
        """Check if the expression can be a number

        :param exp: an expression
        :returns: True if the expression can be a number and false otherwise

        """
        return type(exp) == int or type(exp) == Fraction

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
    for i in a.simplify(render = render):
        print(i)

    print("\n")

def render(tokens):
    post_tokens = Expression.post2in_fix(tokens)
    return ' '.join([str(t) for t in post_tokens])

if __name__ == '__main__':
    exp = "1 + 3 * 5"
    test(exp)

    #exp = "2 * 3 * 3 * 5"
    #test(exp)

    exp = "2 * 3 + 3 * 5"
    test(exp)

    exp = "2 * ( 3 + 4 ) + 3 * 5"
    test(exp)

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

    exp = "( 2 + 5 - 1 ) / ( 3 * 4 )"
    test(exp)

    exp = "( 2 + 5 ) / ( 3 * 4 ) + 1 / 12"
    test(exp)

    exp = "( 2 + 5 ) / ( 3 * 4 ) + 1 / 2"
    test(exp)

    exp = "( 2 + 5 ) / ( 3 * 4 ) + 1 / 12 + 5 * 5"
    test(exp)

    import doctest
    doctest.testmod()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
