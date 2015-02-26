#!/usr/bin/env python
# encoding: utf-8

class Explicable(object):

    """ An Explicable object is an object which can be explicable!
    
    It's a parent class of a more classical Expression, Fraction and Polynom (and later square root)
    Child class will have the following method
        * explain: Generator which return steps which leed to himself
    
    """
    def __init__(self, *args, **kwargs):
        self.steps = []

    def explain(self):
        """ Generate and render steps  which leed to itself """
        old_s = ''
        # les étapes pour l'atteindre
        try:
            for s in self.steps:
                new_s = self.STR_RENDER(s)
                if new_s != old_s:
                    old_s = new_s
                    yield new_s
        except AttributeError:
            pass

        # Lui même
        new_s = self.STR_RENDER(self.postfix_tokens)
        if new_s != old_s:
            yield new_s
        



# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
