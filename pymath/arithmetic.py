#!/usr/bin/env python
# encoding: utf-8


def gcd(a, b):
        """Compute gcd(a,b)

        :param a: first number
        :param b: second number
        :returns: the gcd

        """
        pos_a, _a = (a >= 0), abs(a)
        pos_b, _b = (b >= 0), abs(b)

        gcd_sgn = (-1 + 2*(pos_a or pos_b))

        if _a > _b:
            c = _a % _b
        else:
            c = _b % _a

        if c == 0:
            return gcd_sgn * min(_a,_b)
        elif _a == 1:
            return gcd_sgn * _b
        elif _b == 1:
            return gcd_sgn * _a
        else:
            return gcd_sgn * gcd(min(_a,_b), c)

if __name__ == '__main__':
    print(gcd(3, 15))
    print(gcd(3, 15))
    print(gcd(-15, -3))
    print(gcd(-3, -12))


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
