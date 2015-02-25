#!/usr/bin/env python
# encoding: utf-8

class Renderable_expression(object):

    """Docstring for Renderable_expression. """

    def __init__(self):
        """@todo: to be defined1. """
        



class Computable_expression(Renderable_expression):

    """ A computable_expression is an expression represented by a list of postfix tokens. It's a parent class of a more classical Expression, Fraction and Polynom (and later square root)
    Child class will herits those methods
        * simplify: Compute entirely the expression
        * explain: Generator which return steps which leed to himself
    
    """

    def __init__(self):
        """@todo: to be defined1. """

        pass

    def simplify(self):
        """ Simplify the expression

        :returns: the simplified expression with .steps attributes where steps are stocked

        """
        pass

    def explain(self):
        """ Generate and render steps  which leed to itself """
        pass
        



# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
