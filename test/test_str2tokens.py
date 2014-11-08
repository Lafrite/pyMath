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



if __name__ == '__main__':
    unittest.main()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 

