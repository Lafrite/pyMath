Explication sur la logique des classes
======================================

Les types
---------

Ce sont les objets que l'on s'autorise à manipuler dans les
expressions. Ces objets doivent pouvoir être afficher en *txt* ou en
*tex* avec les méthodes:

 * __txt__ : affichage en mode text
 * __tex__ : affichage pour une compilation latex

Operator
~~~~~~~~

Cette classe regroupe les opérateurs. Que l'on s'autorise à utiliser. On
y accède à partir de deux caractéristiques le symbole et l'arité.

Liste des attributs importants:

 * arity: nombre d'opérande accepté
 * priority: où se place l'opérateur dans la règles des priorités parmi
les autres opérateurs
 * isOperator: permet de vérifier que c'est bien
un opérateur

Liste des méthodes importantes:

 * __call__: Permet d'effectuer le calcul sur deux opérandes
 * __txt__: affichage en mode texte
 * __tex__: affichage pour une compilation latex

Number
~~~~~~

Ce sont tous les types de "nombres" que l'on va vouloir manipuler. On essayera
de rester le plus proche de la construction mathématiques de ces objets.

Par défaut, on travaillera avec des anneaux ce qui permettra de
construire ensuite le corps des fractions et l'anneau des polynômes
(quitte à quotienter) associé.

Pour définir ces anneaux, il faudra contre avoir les méthodes suivantes:

  * __add__ 
  * __radd__ 
  ...

Fractions
^^^^^^^^^

Polynomes
^^^^^^^^^

Quotient de polynomes (racines)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Expression
----------

Render
------

Simplify-simplified / compute-child
-----------------------------------

Dans cette partie, on va expliquer le fonctionnement des mécanismes de
simplification des expressions/objets mathématiques.

La simplification des expressions se fait avec les deux méthodes
suivantes:

-  *simplify()* pour:

   -  un polynôme permet d'accéder à la forme développée d'un polynôme.
   -  une fraction permet d'avoir la fraction irréductible associée.
   -  une expression permet de faire tous les calculs possibles de cette
      expression (à la fin il ne doit y avoir qu'un élément de la liste
      de tokens).

-  *compute_exp()* pour:

   -  un polynôme ou une fraction fait la même chose que `simplify`.
   -  une expression fait tous les calculs élémentaires de cette
      expression.

Ces deux méthodes fonctionnent ensuite sur le même principe. Elles vont
faire le calcul qui leurs est attribué en enregistrant les étapes dans
*steps* puis elles retourneront l'objet de fin de calcul à qui sera
assigné les *steps* (ce qui nécessitera par exemple de détourner la
classe *int*).

Pour accéder à ces étapes, on utilisera alors la méthode *explain* qui
expliqueront les étapes intermédiaires.

