#!/usr/bin/env python
# encoding: utf-8


def gcd(a, b):
		"""Compute gcd(a,b)

		:param a: first number
		:param b: second number
		:returns: the gcd

		"""
		if a > b:
			c = a % b
		else:
			c = b % a

		if c == 0:
			return min(a,b)
		elif a == 1:
			return b
		elif b == 1:
			return a
		else:
			return gcd(min(a,b), c)


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
