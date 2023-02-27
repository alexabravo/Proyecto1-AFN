#Alexa Bravo    18831
#Diseño de Lenguajes de Programación 
#Febrero 2023 

from regex import regex_to_postfix
from nodos import Simbolo, Kleene, Mas, Interrogacion, Or, Concatenacion
import sys
sys.setrecursionlimit(10000)

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

class state: 
    label = None
    edge1 = None
    edge2 = None


class nfa:
    estadoInicial = None
    estadoAceptacion = None

    def __init__(self, estadoInicial, estadoAceptacion):
        self.estadoInicial = estadoInicial
        self.estadoAceptacion = estadoAceptacion


def compilarCadena(postfix):
    nfaStack = []

    for token in postfix:
        if token == '?':
            nfa1 = nfaStack.pop()


            estadoInicial = state()
            estadoAceptacion = state()


            estadoInicial.edge1 = nfa1.estadoInicial
            estadoInicial.edge2 = estadoAceptacion

            nfa1.estadoAceptacion.edge1 = estadoAceptacion

            newNFA = nfa(estadoInicial, estadoAceptacion)
            nfaStack.append(newNFA)
        elif token == '+':

            nfa1 = nfaStack.pop()

            estadoInicial = state()
            estadoAceptacion = state()

            nfa1.estadoAceptacion.edge1 = nfa1.estadoInicial
            nfa1.estadoAceptacion.edge2 = estadoAceptacion

            newNFA = nfa(estadoInicial, estadoAceptacion)
            nfaStack.append(newNFA)

        elif token == '*':
            nfa1 = nfaStack.pop() 

            estadoInicial = state()
            estadoAceptacion = state()

            estadoInicial.edge1 = nfa1.estadoInicial
            estadoInicial.edge2 = estadoAceptacion

            nfa1.estadoAceptacion.edge1 = nfa1.estadoInicial
            nfa1.estadoAceptacion.edge2 = estadoAceptacion

            newNFA = nfa(estadoInicial, estadoAceptacion)
            nfaStack.append(newNFA)
            
        elif token == '.':
            
            nfa2 = nfaStack.pop() 
            nfa1 = nfaStack.pop()

            nfa1.estadoAceptacion.edge1 = nfa2.estadoInicial

            newNFA = nfa(nfa1.estadoInicial, nfa2.estadoAceptacion)
            nfaStack.append(newNFA)
            
        elif token == '|':

            nfa2 = nfaStack.pop() 
            nfa1 = nfaStack.pop()

            estadoInicial = state()

            estadoInicial.edge1 = nfa1.estadoInicial
            estadoInicial.edge2 = nfa2.estadoInicial

            estadoAceptacion = state()

            nfa1.estadoAceptacion.edge1 = estadoAceptacion
            nfa2.estadoAceptacion.edge1 = estadoAceptacion

            newNFA = nfa(estadoInicial, estadoAceptacion)
            nfaStack.append(newNFA)
        else:

            estadoAceptacion = state()
            estadoInicial = state()

            estadoInicial.label = token 
            estadoInicial.edge1 = estadoAceptacion

            newNFA = nfa(estadoInicial, estadoAceptacion)
            nfaStack.append(newNFA)
    
    return nfaStack.pop()

def followArrowE(state):

    states = set()
    states.add(state)

    if state.label is None:

        if state.edge1 is not None:
 
            states |= followArrowE(state.edge1)

        if state.edge2 is not None:

            states |= followArrowE(state.edge2)


    return states


def match(infix, string):

    postfix = regex_to_postfix(infix, False)
    nfa = compilarCadena(postfix)


    currentState = set()
    nextState = set()

    currentState |= followArrowE(nfa.estadoInicial)

    for s in string:

        for c in currentState:
 
            if c.label == s:
  
                nextState |= followArrowE(c.edge1)


        currentState = nextState
        nextState = set()
    
    return(nfa.estadoAceptacion in currentState)
