#!/usr/bin/env python

from distutils.core import setup

setup(name='pyMath',
      version='1.0',
      description='Computing like a student',
      author='Benjamin Bertrand',
      author_email='lafrite@poneyworld.net',
      packages=['pymath'],
      install_requiers=['pyparsing', 'sympy'],
     )
