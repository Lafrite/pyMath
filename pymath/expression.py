#!/usr/bin/env python
# encoding: utf-8

from .generic import Stack, flatten_list, expand_list, isNumber, isOperator
from .render import txt, tex
from .str2tokens import str2tokens

__all__ = ['Expression']

class Expression(object):
    """A calculus expression. Today it can andle only expression with numbers later it will be able to manipulate unknown"""

    STR_RENDER = tex

    def __init__(self, exp):
        """ Initiate the expression

        :param exp: the expression. It can be a string or a list of postfix tokens.
        """
        if type(exp) == str:
            #self._exp = exp
            self.postfix_tokens = str2tokens(exp) # les tokens seront alors stockés dans self.tokens temporairement
        elif type(exp) == list:
            self.postfix_tokens = exp

    def __str__(self):
        """
        Overload str
        If you want to changer render set Expression.RENDER
        """
        return self.STR_RENDER(self.postfix_tokens)

    def render(self, render = lambda  x:str(x)):
        """ Same as __str__ but accept render as argument
        :param render: function which render the list of token (postfix form) to string

        """
        # TODO: I don't like the name of this method |ven. janv. 17 12:48:14 CET 2014
        return render(self.postfix_tokens)

    ## ---------------------
    ## Mechanism functions

    def simplify(self):
        """ Generator which return steps for computing the expression  """
        if not self.can_go_further():
            yield self.STR_RENDER(self.postfix_tokens) 
        else:
            self.compute_exp() 
            old_s = ''
            for s in self.steps:
                new_s = self.STR_RENDER(s)
                # Astuce pour éviter d'avoir deux fois la même étape (par exemple pour la transfo d'une division en fraction)
                if new_s != old_s:
                    old_s = new_s
                    yield new_s
            for s in self.child.simplify():
                if old_s != s:
                    yield s

    def can_go_further(self):
        """Check whether it's a last step or not. If not create self.child the next expression.
        :returns: 1 if it's not the last step, 0 otherwise
        """
        if len(self.postfix_tokens) == 1:
            return 0
        else:
            return 1

    def compute_exp(self):
        """ Create self.child with self.steps to go up to it """
        self.steps = [self.postfix_tokens]

        tokenList = self.postfix_tokens.copy()
        tmpTokenList = []

        while len(tokenList) > 2: 
            # on va chercher les motifs du genre A B +, quand l'operateur est d'arité 2, pour les calculer 
            if isNumber(tokenList[0]) and isNumber(tokenList[1]) \
                    and isOperator(tokenList[2]) and tokenList[2].arity == 2 :
                
                # S'il y a une opération à faire
                op1 = tokenList[0]
                op2 = tokenList[1]
                operator = tokenList[2]

                res = operator(op1, op2)

                tmpTokenList.append(res)

                # Comme on vient de faire le calcul, on peut détruire aussi les deux prochains termes
                del tokenList[0:3]

            # Et les motifs du gens - A, quand l'operateur est d'arité 1
            elif isNumber(tokenList[0]) \
                    and isOperator(tokenList[1]) and tokenList[2].arity == 1:
                
                # S'il y a une opération à faire
                op1 = tokenList[0]
                operator = tokenList[1]

                res = operator(op1)

                tmpTokenList.append(res)

                # Comme on vient de faire le calcul, on peut détruire aussi les deux prochains termes
                del tokenList[0:2]

            else:
                tmpTokenList.append(tokenList[0])

                del tokenList[0]
        tmpTokenList += tokenList

        steps = expand_list(tmpTokenList)

        if len(steps[:-1]) > 0:
            self.steps += [flatten_list(s) for s in steps[:-1]]

        self.child = Expression(steps[-1])


def test(exp):
    a = Expression(exp)
    print(a)
    #for i in a.simplify():
    #    print(i)

    print("\n")

if __name__ == '__main__':
    Expression.STR_RENDER = txt
    exp = "2 ^ 3 * 5"
    test(exp)

    from pymath.operator import add, pw, mul
    exp = [2, 3, pw, 5, mul]
    test(exp)

    exp = "1 + 3 * 5"
    test(exp)

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

    #exp = "( 2 + 5 ) * ( 3 - 4 )^4"
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

    #exp="-2*4(12 + 1)(3-12)"
    #test(exp)


    #exp="(-2+5)/(3*4)+1/12+5*5"
    #test(exp)

    # TODO: The next one doesn't work  |ven. janv. 17 14:56:58 CET 2014
    #exp="-2*(-a)(12 + 1)(3-12)"
    #e = Expression(exp)
    #print(e)

    ## Can't handle it yet!!
    #exp="-(-2)"
    #test(exp)

    #import doctest
    #doctest.testmod()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
