#!/usr/bin/env python
# encoding: utf-8

__report_indent = [0]
def report(fn):
    """Decorator to print information about a function
    call for use while debugging.
    Prints function name, arguments, and call number
    when the function is called. Prints this information
    again along with the return value when the function
    returns.
    """

    def wrap(*params,**kwargs):
        call = wrap.callcount = wrap.callcount + 1

        indent = ' ' * __report_indent[0]
        fc = "%s(%s)" % (fn.__name__, ', '.join(
            [a.__repr__() for a in params] +
            ["%s = %s" % (a, repr(b)) for a,b in kwargs.items()]
        ))

        print( "Call %s%s called [#%s]"
            % (indent, fc, call))
        __report_indent[0] += 1
        ret = fn(*params,**kwargs)
        __report_indent[0] -= 1
        try:
            print(' '*(__report_indent[0]+4), "ret.steps -> ", len(ret.steps))
        except AttributeError:
            print(' '*(__report_indent[0]+4), ret, " has no steps")
        print( "End  %s%s returned %s [#%s]"
            % (indent, fc, repr(ret), call))

        return ret
    wrap.callcount = 0
    return wrap

# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 