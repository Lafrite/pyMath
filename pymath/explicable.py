#!/usr/bin/env python
# encoding: utf-8

from .render import txt, tex

class Renderable(object):
    STR_RENDER = tex
    DEFAULT_RENDER = tex

    @classmethod
    def set_render(cls, render):
        cls.STR_RENDER = render

    @classmethod
    def get_render(cls):
        return cls.STR_RENDER

    @classmethod
    def set_default_render(cls):
        cls.set_render(cls.DEFAULT_RENDER)

    @classmethod
    def tmp_render(cls, render = tex):
        """ Create a container in which Expression render is temporary modify

        The default temporary render is Expression in order to perform calculus inside numbers

        >>> from .expression import Expression
        >>> exp = Expression("2*3/5")
        >>> print(exp)
        2 \\times \\frac{ 3 }{ 5 }
        >>> for i in exp.simplify().explain():
        ...     print(i)
        2 \\times \\frac{ 3 }{ 5 }
        \\frac{ 6 }{ 5 }
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
        class TmpRenderEnv(object):
            def __enter__(self):
                self.old_render = Renderable.get_render()
                Renderable.set_render(render)

            def __exit__(self, type, value, traceback):
                Renderable.set_render(self.old_render)
        return TmpRenderEnv()
        
class Explicable(Renderable):

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
                if hasattr(s, 'postfix_tokens'):
                    new_s = self.STR_RENDER(s.postfix_tokens)
                else:
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
