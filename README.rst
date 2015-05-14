pyMath
======


pyMath est un module python qui permet la manipulation d'expressions
mathématiques. Voici ce qu'il est capable de faire:

-  *Calculer comme un collégien*: Pour faire de la correction automatisé
   d'exercice, un logiciel de calcul formel ne suffit pas. Si les étapes
   de calculs ne sont pas présentes, l'élève ne pourra pas analyser ses
   erreurs ou s'inspirer de la correction.

    .. code-block:: python

        >>> from pymath import Expression
        >>> ajout_fractions = Expression("2 / 5 + 2 / 3")
        >>> resultat = ajout_fractions.simplify()
        >>> print(resultat)
        \frac{ 16 }{ 15 }
        >>> for i in resultat.explain():
        ...      print(i)
        ...
        \frac{ 2 }{ 5 } + \frac{ 2 }{ 3 }
        \frac{ 2 \times 3 }{ 5 \times 3 } + \frac{ 2 \times 5 }{ 3 \times 5 }
        \frac{ 6 }{ 15 } + \frac{ 10 }{ 15 }
        \frac{ 6 + 10 }{ 15 }
        \frac{ 16 }{ 15 }


-  *Créer des exercices aléatoirement*: Pour faire des devoirs
   personnels, des fiches de révisions ou des exercices en classe, un
   générateur d'expressions est inclus.

    .. code-block:: python

                >>> from pymath import Expression
                >>> ajout_fraction = Expression.random("{a} + {b} / {c}")
                >>> print(ajout_fraction)
                2 + \frac{ 3 }{ 5 }

-  *Gérer différents type de données*: Pour le moment, pyMath est
   capable de gérer les entiers naturels, les rationnels (sous forme de
   fractions) et les polynômes. L'utilisation des nombres à virgules et
   des racines devraient être ajoutés dans les prochaines versions.

    .. code-block:: python

                >>> from pymath import Fraction
                >>> une_fraction = Fraction(1,2)
                >>> print(une_fraction)
                1 / 2
                >>> from pymath import Polynom
                >>> un_polynom = Polynom([1,2,3])
                >>> print(un_polynom)
                3 x^{ 2 } + 2 x + 1

-  *Afficher avec deux types de rendus*: Un en mode texte pour
   l'affichage dans une console. Un deuxième spécialement pour écrire
   des documents latex.

    .. code-block:: python

                >>> from pymath import Expression
                >>> ajout_fractions = Expression("2 / 5 + 2 / 3")
                >>> for i in ajout_fractions.simpliy().explain():
                ...      print(i)
                ...
                \frac{ 2 }{ 5 } + \frac{ 2 }{ 3 }
                \frac{ 2 \times 3 }{ 5 \times 3 } + \frac{ 2 \times 5 }{ 3 \times 5 }
                \frac{ 6 }{ 15 } + \frac{ 10 }{ 15 }
                \frac{ 6 + 10 }{ 15 }
                \frac{ 16 }{ 15 }
                >>> from pymath import txt
                >>> with Expression.tmp_render(txt):
                ...      for i in ajout_fractions.simpliy().explain():
                ...          print(i)
                ...
                2 / 5 + 2 / 3
                ( 2 * 3 ) / ( 5 * 3 ) + ( 2 * 5 ) / ( 3 * 5 )
                6 / 15 + 10 / 15
                ( 6 + 10 ) / 15
                16 / 15

    Le rendu latex permet ensuite d'être directement compiler et par exemple d'avoir le rendu suivant

    .. math::
        :nowrap:

            \frac{ 2 }{ 5 } + \frac{ 2 }{ 3 } \\
            \frac{ 2 \times 3 }{ 5 \times 3 } + \frac{ 2 \times 5 }{ 3 \times 5 } \\
            \frac{ 6 }{ 15 } + \frac{ 10 }{ 15 } \\
            \frac{ 6 + 10 }{ 15 } \\
            \frac{ 16 }{ 15 }



Ce module a pour but d'être un outil pour faciliter la construction
d'exercices et leurs correction. Il a pour but d'être le plus simple
possible d'utilisation afin que tout le monde avec un minimum de
connaissance en programmation puisse créer librement des exercices.

