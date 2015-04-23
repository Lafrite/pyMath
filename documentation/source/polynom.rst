Les polynômes
=============

Créer des polynômes
-------------------

Générer un polynôme "fixe"
~~~~~~~~~~~~~~~~~~~~~~~~~~

 .. code-block:: python

    >>> P = Polynom([1,2,3])
    >>> print(P)
    3 x ^ 2 + 2 x + 1
    >>> P = Polynom([1,2,3], letter = 'h')
    >>> print(P)
    3 h ^ 2 + 2 h + 1
    >>> print(P.name)
    'P'
    >>> Q = Polynom([1,2,3], name = 'Q')
    >>> print(Q.name)
    'Q'



Générer un polynôme aléatoirement
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 .. code-block:: python

    >>> P = Polynom.random(["{b}", "{a}"]) # Polynom du type ax + b
    >>> print(P)
    - 8 x - 3
    >>> P = Polynom.random(degree = 2) 
    >>> print(P)
    5 x^{  2 } + 4 x - 7

Manipuler des polynômes
-----------------------

Les représentations des polynômes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 .. code-block:: python

    >>> P = Polynom([1, 2, 3])
    >>> print(P)
    3 x ^ 2 + 2 x + 1

Évaluer des polynômes
~~~~~~~~~~~~~~~~~~~~~

Les polynômes peuvent se comporter comme des fonctions, on peut les évaluer. Il est possible de les évaluer sur des nombres, des expressions et même des polynômes.

Évaluer un polynôme avec un entier
""""""""""""""""""""""""""""""""""

 .. code-block:: python

    >>> type(P(3))
    pymath.expression.Fake_int
    >>> P(3)
    34
    >>> for i in P(3).explain():
        print(i)
    3 \times 3^{  2 } + 2 \times 3 + 1
    3 \times 9 + 6 + 1
    27 + 6 + 1
    33 + 1
    34
    >>> hp1 = Expression('h+1')


Évaluer un polynôme avec une expression
"""""""""""""""""""""""""""""""""""""""

 .. code-block:: python

    >>> type(P(hp1))
    < <class 'pymath.polynomDeg2.Polynom_deg2'> [6, 8, 3]>
    >>> print(P(hp1))
    3 h ^ 2 + 8 h + 6
    >>> for i in P(hp1).explain():
    ...     print(i)
    ...
    3 ( h + 1 )^{  2 } + 2 ( h + 1 ) + 1
    3 ( h + 1 ) ( h + 1 ) + 2 h + 2 + 1
    3 ( h^{  2 } + ( 1 + 1 ) h + 1 ) + 2 h + 2 + 1
    3 ( h^{  2 } + 2 h + 1 ) + 2 h + 2 + 1
    3 ( h^{  2 } + 2 h + 1 ) + 2 ( h + 1 ) + 1
    3 h^{  2 } + 3 \times 2 h + 3 + 2 h + 2 + 1
    3 h^{  2 } + 6 h + 3 + 2 h + 2 + 1
    3 h^{  2 } + ( 6 + 2 ) h + 3 + 2 + 1
    3 h^{  2 } + 8 h + 5 + 1
    3 h^{  2 } + 8 h + 6

Évaluer un polynôme avec un autre polynôme
""""""""""""""""""""""""""""""""""""""""""

.. code-block:: python

    >>> type(P(P))
    pymath.polynom.Polynom
    >>> print(P(P))
    27 x ^ 4 + 36 x ^ 3 + 36 x ^ 2 + 16 x + 6
    >>> for i in P(P).explain():
    ...     print(i)
    ...
    3 ( 3 x^{  2 } + 2 x + 1 )^{  2 } + 2 ( 3 x^{  2 } + 2 x + 1 ) + 1
    3 ( 3 x^{  2 } + 2 x + 1 ) ( 3 x^{  2 } + 2 x + 1 ) + 2 \times 3 x^{  2 } + 2 \times 2 x + 2 + 1
    3 ( 3 \times 3 x^{  4 } + ( 2 \times 3 + 3 \times 2 ) x^{  3 } + ( 3 + 2 \times 2 + 3 ) x^{  2 } + ( 2 + 2 ) x + 1 ) + 6 x^{  2 } + 4 x + 2 + 1
    3 ( 9 x^{  4 } + ( 6 + 6 ) x^{  3 } + ( 3 + 4 + 3 ) x^{  2 } + 4 x + 1 ) + 6 x^{  2 } + 4 x + 2 + 1
    3 ( 9 x^{  4 } + 12 x^{  3 } + ( 7 + 3 ) x^{  2 } + 4 x + 1 ) + 6 x^{  2 } + 4 x + 2 + 1
    3 ( 9 x^{  4 } + 12 x^{  3 } + 10 x^{  2 } + 4 x + 1 ) + 6 x^{  2 } + 4 x + 2 + 1
    3 ( 9 x^{  4 } + 12 x^{  3 } + 10 x^{  2 } + 4 x + 1 ) + 2 ( 3 x^{  2 } + 2 x + 1 ) + 1
    3 \times 9 x^{  4 } + 3 \times 12 x^{  3 } + 3 \times 10 x^{  2 } + 3 \times 4 x + 3 + 2 \times 3 x^{  2 } + 2 \times 2 x + 2 + 1
    27 x^{  4 } + 36 x^{  3 } + 30 x^{  2 } + 12 x + 3 + 6 x^{  2 } + 4 x + 2 + 1
    27 x^{  4 } + 36 x^{  3 } + ( 30 + 6 ) x^{  2 } + ( 12 + 4 ) x + 3 + 2 + 1
    27 x^{  4 } + 36 x^{  3 } + 36 x^{  2 } + 16 x + 5 + 1
    27 x^{  4 } + 36 x^{  3 } + 36 x^{  2 } + 16 x + 6


Opération et polynômes
~~~~~~~~~~~~~~~~~~~~~~

Les opérations +, -, \* et ^ sont accessibles aux polynômes. Elles renvoient *toujours* un polynôme (même si le résultat est une constante)

 .. code-block:: python

    >>> type(P + 1)
    pymath.polynomDeg2.Polynom_deg2
    >>> for i in (P+1).explain():
        print(i)
    3 x^{  2 } + 2 x + 1 + 1
    3 x^{  2 } + 2 x + 2
    >>> Q = Polynom([4, 5, 6])
    >>> for i in (P+Q).explain():
        print(i)
    3 x^{  2 } + 2 x + 1 + 6 x^{  2 } + 5 x + 4
    ( 3 + 6 ) x^{  2 } + ( 2 + 5 ) x + 1 + 4
    9 x^{  2 } + 7 x + 5
    >>> Q = Polynom([0,2,3])
    >>> print(Q)
    >>> print(P-Q)
    1
    >>> type(P-Q)
    pymath.polynom.Polynom

Dérivation
~~~~~~~~~~

Il est possible de dériver les polynômes à partir de la méthode *derivate*. De la même façon que pour les opérations, le polynôme dérivé pour s'expliquer avec la méthode *explain*.

 .. code-block:: python

    >>> P1 = P.derivate()
    >>> print(P1)
    6 x + 2
    >>> for i in P1.explain():
    ...     print(i)
    ...
    2 \times 3 x + 1 \times 2
    6 x + 2
    >>> print(P1.name)
    "P'"

Polynomes du second degré
-------------------------

Les polynômes du second degré héritent de toutes les méthodes venant de la classe Polynom. Ils ont cependant accès à d'autres méthodes plus spécifiques aux polynômes de ce degré:

    * Accès aux coefficients de façon 'naturelle'
    * *delta*: discriminant du polynôme.
    * *alpha*: Abscisse de l'extremum.
    * *beta*: ordonnée de l'extremum.
    * *roots*: les racines du polynôme (/!\ utilise *sympy* et ne peux pas expliquer le calcul pour le moment)
    * *tbl_sgn_header*: en-tête du tableau du tableau de signe écrit pour *TkzTab*
    * *tbl_sgn*: ligne du tableau de signe pour *TkzTab*
    * *tbl_variation*: ligne du tableau de variation pour *TkzTab*

Packages
--------

Abstact_polynom
~~~~~~~~~~~~~~~

.. automodule:: pymath.abstact_polynom
