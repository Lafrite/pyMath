#!/usr/bin/env python
# encoding: utf-8

from .generic import Stack, flatten_list, expand_list, isNumber, isOperator, isNumerand
from .str2tokens import str2tokens
from .operator import op
from .explicable import Explicable

from .random_expression import RdExpression

__all__ = ['Expression']


class Expression(Explicable):
    """A calculus expression. Today it can andle only expression with numbers later it will be able to manipulate unknown"""


    @classmethod
    def random(self, form="", conditions=[], val_min = -10, val_max=10):
        """Create a random expression from form and with conditions

        :param form: the form of the expression (/!\ variables need to be in brackets {})
        :param conditions: condition on variables (/!\ variables need to be in brackets {})
        :param val_min: min value for generate variables
        :param val_max: max value for generate variables

        """
        random_generator = RdExpression(form, conditions)
        return Expression(random_generator(val_min, val_max))

    @classmethod
    def tmp_render(cls, render = lambda _,x:Expression(x)):
        """ Same ad tmp_render for Renderable but default render is Expression

        >>> exp = Expression("2*3/5")
        >>> print(exp)
        2 \\times \\frac{ 3 }{ 5 }
        >>> for i in exp.simplify().explain():
        ...     print(i)
        2 \\times \\frac{ 3 }{ 5 }
        \\frac{ 6 }{ 5 }
        >>> with Expression.tmp_render():
        ...     for i in exp.simplify().explain():
        ...         i
        < <class '__main__.Expression'> [2, 3, 5, '/', '*'] >
        < <class '__main__.Expression'> [2, < Fraction 3 / 5>, '*'] >
        < <class '__main__.Expression'> [2, < Fraction 3 / 5>, '*'] >
        < <class '__main__.Expression'> [6, 5, '/'] >
        >>> from .render import txt
        >>> with Expression.tmp_render(txt):
        ...     for i in exp.simplify().explain():
        ...         print(i)
        2 * 3 / 5
        6 / 5
        >>> for i in exp.simplify().explain():
        ...     print(i)
        2 \\times \\frac{ 3 }{ 5 }
        \\frac{ 6 }{ 5 }

        """
        return super(Expression, cls).tmp_render(render)

    def __new__(cls, exp):
        """Create Expression objects

        :param exp: the expression. It can be a string or a list of postfix tokens.

        """
        expression = object.__new__(cls)
        if type(exp) == str:
            expression.postfix_tokens = str2tokens(exp) 
        elif type(exp) == list:
            expression.postfix_tokens = flatten_list([tok.postfix_tokens if Expression.isExpression(tok) else tok for tok in exp])
        elif type(exp) == Expression:
            return exp 
        else:
            raise ValueError("Can't build Expression with {} object".format(type(exp)))

        if len(expression.postfix_tokens) == 1:
            token = expression.postfix_tokens[0]
            if hasattr(token, 'simplify') and hasattr(token, 'explain'):
                return expression.postfix_tokens[0]

            elif type(token) == int:
            # On crée un faux int en ajoutant la méthode simplify et simplified et la caractérisique isNumber
                simplify = lambda x:x
                is_number = True
                methods_attr = {'simplify':simplify, 'isNumber': is_number, 'postfix_tokens': [token]}
                fake_token = type('fake_int', (int,Explicable, ), methods_attr)(token)
                return fake_token

            elif type(token) == str:
                # TODO: Pourquoi ne pas créer directement un polynom ici? |jeu. févr. 26 18:59:24 CET 2015
            # On crée un faux str en ajoutant la méthode simplify et simplified et la caractérisique isNumber
                simplify = lambda x:[x]
                is_polynom = True
                methods_attr = {'simplify':simplify, '_isPolynom': is_polynom, 'postfix_tokens': [token]}
                fake_token = type('fake_str', (str,Explicable, ), methods_attr)(token)
                return fake_token
            else:
                raise ValueError("Unknow type in Expression: {}".format(type(token)))

        else:
            expression._isExpression = 1
            return expression

    def __str__(self):
        """
        Overload str

        If you want to changer render use Expression.set_render(...) or use tmp_render context manager.
        """
        return self.STR_RENDER(self.postfix_tokens)

    def __repr__(self):
        return " ".join(["<", str(self.__class__) , str(self.postfix_tokens), ">"])

    def simplify(self):
        """ Compute entirely the expression and return the result with .steps attribute """
        self.compute_exp()

        self.simplified = self.child.simplify()
        try:
            self.simplified.steps = self.child.steps + self.simplified.steps
        except AttributeError:
            pass

        return self.simplified

    def compute_exp(self):
        """ Create self.child with and stock steps in it """
        child_steps = [self.postfix_tokens]

        tokenList = self.postfix_tokens.copy()
        tmpTokenList = []

        while len(tokenList) > 2: 
            # on va chercher les motifs du genre A B +, quand l'operateur est d'arité 2, pour les calculer 
            if isNumerand(tokenList[0]) and isNumerand(tokenList[1]) \
                    and isOperator(tokenList[2]) and tokenList[2].arity == 2 :
                
                # S'il y a une opération à faire
                op1 = tokenList[0]
                op2 = tokenList[1]
                operator = tokenList[2]
                
                res = operator(op1, op2)

                tmpTokenList.append(res)

                # Comme on vient de faire le calcul, on peut détruire aussi les deux prochains termes
                del tokenList[0:3]

            # Et les motifs du gens A -, quand l'operateur est d'arité 1
            elif isNumerand(tokenList[0]) \
                    and isOperator(tokenList[1]) and tokenList[1].arity == 1:
                
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

        if len(tokenList) == 2 and isNumerand(tokenList[0]) \
                    and isOperator(tokenList[1]) and tokenList[1].arity == 1:
            # S'il reste deux éléments dont un operation d'arité 1
            op1 = tokenList[0]
            operator = tokenList[1]

            res = operator(op1)

            tmpTokenList.append(res)

            # Comme on vient de faire le calcul, on peut détruire aussi les deux prochains termes
            del tokenList[0:2]

        tmpTokenList += tokenList

        steps = expand_list(tmpTokenList)

        if len(steps[:-1]) > 0:
            child_steps += [flatten_list(s) for s in steps[:-1]]

        self.child = Expression(steps[-1])
        self.child.steps = child_steps

    @classmethod
    def isExpression(self, other):
        try:
            other._isExpression
        except AttributeError:
                return 0
        return  1

    # -----------
    # Expression act as container from self.postfix_tokens

    def __getitem__(self, index):
        return self.postfix_tokens[index]

    def __setitem__(self, index, value):
        self.postfix_tokens[index] = value

    # -----------
    # Some math manipulations

    def operate(self, other, operator):
        if type(other) == Expression:
            return Expression(self.postfix_tokens + other.postfix_tokens + [operator])
        elif type(other) == list:
            return Expression(self.postfix_tokens + other + [operator])
        else:
            return Expression(self.postfix_tokens + [other] + [operator])
    
    def roperate(self, other, operator):
        if type(other) == Expression:
            return Expression(other.postfix_tokens + self.postfix_tokens + [operator])
        elif type(other) == list:
            return Expression(other + self.postfix_tokens + [operator])
        else:
            return Expression([other] + self.postfix_tokens + [operator])

    def __add__(self, other):
        """ Overload +

        >>> a = Expression("1+2")
        >>> print(a.postfix_tokens)
        [1, 2, '+']
        >>> b = Expression("3+4")
        >>> print(b.postfix_tokens)
        [3, 4, '+']
        >>> c = a + b
        >>> print(c.postfix_tokens)
        [1, 2, '+', 3, 4, '+', '+']
        """
        return self.operate(other, op.add)

    def __radd__(self, other):
        return self.roperate(other, op.add)

    def __sub__(self, other):
        """ Overload -

        >>> a = Expression("1+2")
        >>> print(a.postfix_tokens)
        [1, 2, '+']
        >>> b = Expression("3+4")
        >>> print(b.postfix_tokens)
        [3, 4, '+']
        >>> c = a - b
        >>> print(c.postfix_tokens)
        [1, 2, '+', 3, 4, '+', '-']
        """
        return self.operate(other, op.sub)

    def __rsub__(self, other):
        return self.roperate(other, op.sub)

    def __mul__(self, other):
        """ Overload *

        >>> a = Expression("1+2")
        >>> print(a.postfix_tokens)
        [1, 2, '+']
        >>> b = Expression("3+4")
        >>> print(b.postfix_tokens)
        [3, 4, '+']
        >>> c = a * b
        >>> print(c.postfix_tokens)
        [1, 2, '+', 3, 4, '+', '*']
        """
        return self.operate(other, op.mul)

    def __rmul__(self, other):
        return self.roperate(other, op.mul)

    def __truediv__(self, other):
        """ Overload /

        >>> a = Expression("1+2")
        >>> print(a.postfix_tokens)
        [1, 2, '+']
        >>> b = Expression("3+4")
        >>> print(b.postfix_tokens)
        [3, 4, '+']
        >>> c = a / b
        >>> print(c.postfix_tokens)
        [1, 2, '+', 3, 4, '+', '/']
        >>> 
        """
        return self.operate(other, op.div)

    def __rtruediv__(self, other):
        return self.roperate(other, op.div)

    def __pow__(self, other):
        return self.operate(other, op.pw)

    def __xor__(self, other):
        return self.operate(other, op.pw)

    def __neg__(self):
        return Expression(self.postfix_tokens + [op.sub1])
    

def test(exp):
    a = Expression(exp)
    b = a.simplify()

    for i in b.explain():
        #print(type(i))
        print(i)

    #print(type(a.simplified()), ":", a.simplified())

    print("\n")

if __name__ == '__main__':
    #render = lambda _,x : str(x)
    #Expression.set_render(render)
    #exp = Expression("1/2 - 4")
    #print(list(exp.simplify()))

    #Expression.set_render(txt)
    #exp = "2 ^ 3 * 5"
    #test(exp)

    #exp = "2x + 5"
    #test(exp)

    #Expression.set_render(tex)

    #test(exp1)

    #from pymath.operator import op
    #exp = [2, 3, op.pw, 5, op.mul]
    #test(exp)

    #test([Expression(exp1), Expression(exp), op.add])

    #exp = "1 + 3 * 5"
    #e = Expression(exp)
    #f = -e
    #print(f)

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

    #print("\n")
    #exp = Expression.random("({a} + 3)({b} - 1)", ["{a} > 4"])
    #for i in exp.simplify():
    #    print(i)

    import doctest
    doctest.testmod()

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
