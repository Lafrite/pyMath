#!/usr/bin/env python
# encoding: utf-8


import unittest

from pymath.str2tokens import str2tokens, str2in_tokens, in2post_fix

class TestStr2tokens(unittest.TestCase):
    """Testing functions from pymath.str2tokens"""

    def test_str2intokens(self):
        ans = str2in_tokens("2+3*4")
        self.assertEqual(ans, [2, "+", 3, "*", 4])
        
        ans = str2in_tokens("2*3+4")
        self.assertEqual(ans, [2, "*", 3, "+", 4])
        

    def test_in2post_fix(self):
        in_tokens = str2in_tokens("2+3*4")
        ans = in2post_fix(in_tokens)
        self.assertEqual(ans, [2, 3, 4, "*", "+"])
        
        in_tokens = str2in_tokens("2*3+4")
        ans = in2post_fix(in_tokens)
        self.assertEqual(ans, [2, 3,"*", 4, "+"])
        

        # TODO: Ajouter des tests pour les cas particuliers... |sam. nov.  8 17:39:18 CET 2014
    def test_str2in_tokens_big_num(self):
        exp = "123 + 3"
        tok = str2in_tokens(exp)
        self.assertEqual(tok, [123, "+", 3])

    def test_str2in_tokens_beg_minus(self):
        exp = "-123 + 3"
        tok = str2in_tokens(exp)
        self.assertEqual(tok, [-123, "+", 3])

    def test_str2in_tokens_time_lack(self):
        exp = "(-3)(2)"
        tok = str2in_tokens(exp)
        self.assertEqual(tok, ["(", -3, ")", "*","(", 2, ")" ])

    def test_str2in_tokens_time_lack2(self):
        exp = "-3(2)"
        tok = str2in_tokens(exp)
        self.assertEqual(tok, [-3, "*","(", 2, ")" ])

    def test_str2tokens_error_float(self):
        exp = "1 + 1.3"
        self.assertRaises(ValueError, str2tokens, exp)

    def test_str2tokens_error(self):
        exp = "1 + $"
        self.assertRaises(ValueError, str2tokens, exp)



if __name__ == '__main__':
    unittest.main()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

