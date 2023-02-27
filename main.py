from regex import regex_to_postfix
from thompson import compileNFA
from afn import AFN
from graphviz import Source, render
from contextlib import redirect_stdout


DEBUG = False


def validate_expr(expr):

	operators = ["+", "|", "*", "?"]
	err = []

	cn_1 = 0
	cn_2 = 0

	for i in range(len(expr) - 1):
		if expr[i] == "(":
			cn_1 += 1
		elif expr[i] in operators and expr[i+1] in operators:
				print("Hay dos operadores juntos en la expresión")
				return False

	for n in expr:
		if n == ")":
			cn_2 += 1

	if cn_1 == cn_2:
		pass
	else:
		print("Falta un parentesis")
		return False



if __name__ == '__main__':

	eleccion = True
	options = [1,2,3]

	while(eleccion):
		secondEleccion = False
		print("		1. Thompson")
		print("		2. Ver grafo")
		print("		3. Salir")

		try:
			opcion = int(input("Escoja una opción: "))
			if opcion in options:
				segundaEleccion = True
			else:
				print("\nIngrese una opcion valida\n")
		except ValueError as e:
			print("\nSolo números\n")

		if segundaEleccion:
			if opcion == 1:
				#Pedimos a usuario la expresion regular
				expresion_regular = input("Expresion regular: ")

				if validate_expr(expresion_regular) == False:
					break;
				
				postfix = regex_to_postfix(expresion_regular)
				nfa = compileNFA(postfix)
				nfa_real = AFN(nfa[0])
				with open('afn.gv', 'w', encoding="utf-8") as f:
					with redirect_stdout(f):
						nfa_real.print_graphviz()

			elif opcion == 2:
				filename = input("Archivo: ")

				src = Source.from_file(filename)
				src.render('graph.gv', view=True)
			
			elif opcion == 3:
				eleccion = False
				segundaEleccion = False
				