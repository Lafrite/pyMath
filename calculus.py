#!/usr/bin/env python
# encoding: utf-8


from generic import Stack



def infixToPostfix(infixExp):
	"""Transform an infix expression into postfix expression

	:param infixExp: an infix expression (caracters must be separate by a space)
	:returns: the corresponding postfix expression

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
	print(postfixToInfix(postfixExp))
	# where to save numbers or 
	operandeStack = Stack()

	tokenList = postfixExp.split(" ")

	while len(tokenList) > 1:
		tmpTokenList = []
		i = 0
		while len(tokenList) > 2: 
			if (tokenList[1].isdigit() or (tokenList[1][0] == "-" and tokenList[1][1:].isdigit())) and tokenList[2] in "+-*/":
				# S'il y a une opération à faire
				op1 = tokenList[0]
				op2 = tokenList[1]
				token = tokenList[2]
				res = doMath(token, op1, op2)

				tmpTokenList.append(res)
				# Comme on vient de faire le calcul, on peut sauter les deux prochains termes
				i += 3

				del tokenList[0:3]
			else:
				tmpTokenList.append(tokenList[0])
				i += 1

				del tokenList[0]
		tmpTokenList += tokenList

		tokenList = tmpTokenList.copy()
		print(postfixToInfix(" ".join(tokenList)))

	return tokenList[0]

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
	priority = {"*" : 3, "/": 3, "+": 2, "-":2}
	operandeStack = Stack()

	tokenList = postfixExp.split(" ")

	for (i,token) in enumerate(tokenList):
		if token in "+-*/":
			op2 = operandeStack.pop()
			op1 = operandeStack.pop()
			res = "{op1} {op} {op2}".format(op1 = op1, op = token, op2 = op2)
			
			parenthesis = False
			if i+1 < len(tokenList):
				if tokenList[i+1] in "+-*/":
					if priority[token] < priority[tokenList[i+1]]:
						res = "( " + res + " )"
						parenthesis = True 
			if i+2 < len(tokenList) and not parenthesis:
				if tokenList[i+2] in "+-*/":
					if priority[token] < priority[tokenList[i+2]]:
						res = "( " + res + " )"

			operandeStack.push(res)

			#print("new token: {token}".format(token = token))
			#print(" ".join(operandeStack +["!!"]+ tokenList[i+1:]))

		else:
			operandeStack.push(token)

	return operandeStack.pop()


def test(exp):
	"""Make various test on an expression

	"""
	print("-------------")
	print("Expression ",exp)
	postfix = infixToPostfix(exp)
	print("Postfix " , postfix)
	print(computePostfix(postfix))
	print("Bis")
	print(computePostfixBis(postfix))
	#print(postfixToInfix(postfix))


if __name__ == '__main__':
	exp = "1 + 3 * 5"
	test(exp)

	exp = "2 * 3 + 3 * 5"
	test(exp)

	exp = "2 * ( 3 + 4 ) + 3 * 5"
	test(exp)
	
	exp = "2 * ( 3 + 4 ) + ( 3 - 4 ) * 5"
	test(exp)
	
	exp = "2 * ( 2 - ( 3 + 4 ) ) + ( 3 - 4 ) * 5"
	test(exp)
	
	exp = "2 * ( 2 - ( 3 + 4 ) ) + 5 * ( 3 - 4 )"
	test(exp)
	
	exp = "2 + 5 * ( 3 - 4 )"
	test(exp)


# -----------------------------
# Reglages pour 'vim'
# vim:set autoindent expandtab tabstop=4 shiftwidth=4:
# cursor: 16 del 
