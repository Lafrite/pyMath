#!/usr/bin/env python
# encoding: utf-8


from generic import Stack



def infixToPostfix(infixExp):
    """Transform an infix expression into postfix expression

    :param infixExp: an infix expression (caracters must be separate by a space)
    :returns: the corresponding postfix expression

    :Example:

    >>> infixToPostfix("1 + 2")
    '1 2 +'

    >>> infixToPostfix("1 * 2 + 3")
    '1 2 * 3 +'

    """
    priority = {"*" : 3, "/": 3, "+": 2, "-":2, "(": 1}
    
    opStack = Stack()
    postfixList = []

    tokenList = infixExp.split(" ")

    for token in tokenList:
        if token == "(":
            opStack.push(token)
        elif token == ")":
            topToken = opStack.pop()
            while topToken != "(":
                postfixList.append(topToken)
                topToken = opStack.pop()
        elif token in "+-*/":
            while (not opStack.isEmpty()) and (priority[opStack.peek()] >= priority[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)
        else:
            postfixList.append(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())

    return " ".join(postfixList)

def computePostfix(postfixExp):
    """Compute a postfix expression

    :param postfixExp: a postfix expression
    :returns: the result of the expression

    """
    print(postfixToInfix(postfixExp))
    # where to save numbers or 
    operandeStack = Stack()

    tokenList = postfixExp.split(" ")

    for (i,token) in enumerate(tokenList):
        if token in "+-*/":
            op2 = operandeStack.pop()
            op1 = operandeStack.pop()
            res = doMath(token, op1, op2)
            operandeStack.push(res)

            #print("Operation: {op1} {op} {op2}".format(op1 = op1, op = token, op2 = op2))
            #print(operandeStack)
            #print(tokenList[i+1:])
            newPostfix = " ".join(operandeStack + tokenList[i+1:])
            print(postfixToInfix(newPostfix))

        else:
            operandeStack.push(token)

    return operandeStack.pop()

def computePostfixBis(postfixExp):
    """Compute a postfix expression like a good student

    :param postfixExp: a postfix expression
    :returns: the result of the expression

    """
    print(postfixExp)
    print(postfixToInfix(postfixExp))
    # where to save numbers or 
    operandeStack = Stack()

    tokenList = postfixExp.split(" ")

    steps = []

    # On fait le calcul jusqu'à n'avoir plus qu'un élément
    while len(tokenList) > 1:
        tmpTokenList = []
        # on va chercher les motifs du genre A B + pour les calculer
        while len(tokenList) > 2: 
            if isNumber(tokenList[0]) and isNumber(tokenList[1]) and tokenList[2] in "+-*/":
                # S'il y a une opération à faire
                op1 = tokenList[0]
                op2 = tokenList[1]
                token = tokenList[2]
                res = doMath(token, op1, op2)

                tmpTokenList.append(res)

                # Comme on vient de faire le calcul, on peut détruire aussi les deux prochains termes
                del tokenList[0:3]
            else:
                tmpTokenList.append(tokenList[0])

                del tokenList[0]
        tmpTokenList += tokenList

        steps += expand_list(tmpTokenList)
        #print("----- Steps -----")
        #print(steps)

        tokenList = steps[-1]

        #print(postfixToInfix(tokenList))

    return steps

def isNumber(exp):
    """Check if the expression can be a number

    :param exp: an expression
    :returns: True if the expression can be a number and false otherwise

    """
    return type(exp) == int or type(exp) == "Fraction"

def isOperation(exp):
    """Check if the expression is an opération in "+-*/"

    :param exp: an expression
    :returns: boolean

    """
    return (type(exp) == str and exp in "+-*/")


def doMath(op, op1, op2):
    """Compute "op1 op op2"

    :param op: operator
    :param op1: first operande
    :param op2: second operande
    :returns: string representing the result

    """
    return str(eval(op1 + op + op2))


def postfixToInfix(postfixExp):
    """Transforme postfix expression into infix expression

    :param postfixExp: a postfix expression
    :returns: the corresponding infix expression

    """
    operandeStack = Stack()

    tokenList = postfixExp.split(" ")

    for (i,token) in enumerate(tokenList):
        if token in "+-*/":
            op2 = operandeStack.pop()
            if needPar(op2, token, "after"):
                op2 = "( " + op2 + " )"
            op1 = operandeStack.pop()
            if needPar(op1, token, "before"):
                op1 = "( " + op1 + " )"
            res = "{op1} {op} {op2}".format(op1 = op1, op = token, op2 = op2)

            operandeStack.push(res)

        else:
            operandeStack.push(token)

    return operandeStack.pop()

def needPar(operande, operator, posi = "after"):
    """Says whether or not the operande needs parenthesis

    :param operande: the operande
    :param operator: the operator
    :param posi: "after"(default) if the operande will be after the operator, "before" othewise
    :returns: bollean
    """
    priority = {"*" : 3, "/": 3, "+": 2, "-":2}

    if type(operande)==int and operande < 0:
        return 1
    elif not isNumber(operande):
        # Si c'est une grande expression ou un chiffre négatif
        stand_alone = get_main_op(operande)
        # Si la priorité de l'operande est plus faible que celle de l'opérateur
        debug_var("stand_alone",stand_alone)
        debug_var("operande", type(operande))
        minor_priority = priority[get_main_op(operande)] < priority[operator]
        # Si l'opérateur est -/ pour after ou juste / pour before
        special = (operator in "-/" and posi == "after") or (operator in "/" and posi == "before")

        return stand_alone and (minor_priority or special)
    else:
        return 0

def get_main_op(exp):
    """Getting the main operation of the expression

    :param exp: the expression
    :returns: the main operation (+, -, * or /) or 0 if the expression is only one element

    """

    priority = {"*" : 3, "/": 3, "+": 2, "-":2}

    parStack = Stack()
    tokenList = exp.split(" ")

    if len(tokenList) == 1:
    # Si l'expression n'est qu'un élément
        return 0

    main_op = []

    for token in tokenList:
        if token == "(":
            parStack.push(token)
        elif token == ")":
            parStack.pop()
        elif token in "+-*/" and parStack.isEmpty():
            main_op.append(token)

    return min(main_op, key = lambda s: priority[s])


def expand_list(list_list):
    """Expand list of list

    :param list: the list to expande
    :returns: list of expanded lists

    :Example:

    >>> expand_list([1,2,[3,4],5,[6,7,8]])
    [[1, 2, 3, 5, 6], [1, 2, 4, 5, 7], [1, 2, 4, 5, 8]]
    >>> expand_list([1,2,4,5,6,7,8])
    [[1, 2, 4, 5, 6, 7, 8]]

    """
    list_in_list = [i for i in list_list if type(i) == list].copy()

    try:
        nbr_ans_list = max([len(i) for i in list_in_list])

        ans = [list_list.copy() for i in range(nbr_ans_list)]
        for (i,l) in enumerate(ans):
            for (j,e) in enumerate(l):
                if type(e) == list:
                    ans[i][j] = e[min(i,len(e)-1)]
    # S'il n'y a pas eut d'étapes intermédiaires (2e exemple)
    except ValueError:
        ans = [list_list]

    return ans

def print_steps(steps):
    """Juste print a list

    :param steps: @todo
    :returns: @todo

    """
    print("{first} \t = {sec}".format(first = steps[-1], sec = steps[-2]))
    for i in steps[-2:0:-1]:
        print("\t\t = ",i)


def debug_var(name, var):
    """print the name of the variable and the value

    :param name: the name of the variable
    :param var: the variable we want information
    """
    print(name, ": ", var)


def test(exp):
    """Make various test on an expression

    """
    print("-------------")
    print("Expression ",exp)
    postfix = infixToPostfix(exp)
    #print("Postfix " , postfix)
    #print(computePostfix(postfix))
    #print("Bis")
    steps = computePostfixBis(postfix)
    print_steps(steps)
    #print(postfixToInfix(postfix))
    #print(get_main_op(exp))


if __name__ == '__main__':
    exp = "1 + 3 * 5"
    test(exp)

    #exp = "2 * 3 * 3 * 5"
    #test(exp)

    #exp = "2 * 3 + 3 * 5"
    #test(exp)

    #exp = "2 * ( 3 + 4 ) + 3 * 5"
    #test(exp)
    #
    #exp = "2 * ( 3 + 4 ) + ( 3 - 4 ) * 5"
    #test(exp)
    #
    #exp = "2 * ( 2 - ( 3 + 4 ) ) + ( 3 - 4 ) * 5"
    #test(exp)
    #
    #exp = "2 * ( 2 - ( 3 + 4 ) ) + 5 * ( 3 - 4 )"
    #test(exp)
    #
    #exp = "2 + 5 * ( 3 - 4 )"
    #test(exp)
    #
    #exp = "( 2 + 5 ) * ( 3 - 4 )"
    #test(exp)
    #
    #exp = "( 2 + 5 ) * ( 3 * 4 )"
    #test(exp)
    
    exp = "( 2 + 5 - 1 ) / ( 3 * 4 )"
    test(exp)

    exp = "( 2 + 5 ) / ( 3 * 4 ) + 1 / 12"
    test(exp)

    exp = "( 2 + 5 ) / ( 3 * 4 ) + 1 / 2"
    test(exp)

    exp = "( 2 + 5 ) / ( 3 * 4 ) + 1 / 12 + 5 * 5"
    test(exp)

    #print(expand_list([1,2,['a','b','c'], 3, ['d','e']]))
    
    ## Ce denier pose un soucis. Pour le faire marcher il faudrai implémenter le calcul avec les fractions
    #exp = "( 2 + 5 ) / 3 * 4"
    #test(exp)
    #import doctest
    #doctest.testmod()


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
