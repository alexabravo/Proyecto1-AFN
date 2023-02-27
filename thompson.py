

from nodos import Simbolo, Kleene, Mas, Interrogacion, Or, Concatenacion

#Dedinimos los simbolos

symbols = {
	0: "?",
	1: "+",
	2: "*",
	3: "|",
	4: ".",
    5: "^",
}

#Compilamos el postfix a NFA 
def compileNFA(pfix):
	nfaStack = []

	print("\nLa expresión en postfix es: ", pfix) 
	for token in pfix:
		if token == '?':
			nfa = nfaStack.pop()
			#Va al stack de NFA 
			newNFA = Interrogacion(symbols[0])
			nfaStack.append(newNFA.thompson(nfa[0], nfa[1]))
		elif token == '+':
			nfa = nfaStack.pop()
			newNFA = Mas(symbols[1])
			nfaStack.append(newNFA.thompson(nfa[0], nfa[1]))
		elif token == '*':
			nfa = nfaStack.pop()
			newNFA = Kleene(symbols[2])
			nfaStack.append(newNFA.thompson(nfa[0], nfa[1]))
		elif token == '.':
			nfa1 = nfaStack.pop()
			nfa2 = nfaStack.pop()
			newNFA = Concatenacion(symbols[4], nfa1, nfa2)
			nfaStack.append(newNFA.thompson())
		elif token == '|':
			nfa1 = nfaStack.pop()
			nfa2 = nfaStack.pop()
			newNFA = Or(symbols[3], nfa1, nfa2)
			nfaStack.append(newNFA.thompson())
		else:
			newNFA = Simbolo(token)
			nfaStack.append(newNFA.thompson())

	return nfaStack.pop()