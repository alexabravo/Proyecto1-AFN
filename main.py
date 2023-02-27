#Alexa Bravo    18831
#Diseño de Lenguajes de Programación 
#Febrero 2023 

from regex import regex_to_postfix
from thompson import compileNFA, match
from afn import AFN
from graphviz import Source, render
from contextlib import redirect_stdout

def validarExpresion(exp):

	operators = ["+", "|", "*", "?", ";"]
	err = []

	simbolo1 = 0
	simbolo2 = 0

	for i in range(len(exp) - 1):
		if exp[i] == "(":
			simbolo1 += 1
		elif exp[i] in operators and exp[i+1] in operators:
				print("Hay dos operadores juntos")
				return False

	for n in exp:
		if n == ")":
			simbolo2 += 1 

	if simbolo1 == simbolo2:
		pass
	else:
		print("Falta un parentesis en la expresión")
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
			opcion = int(input("Elija una opción: "))
			if opcion in options:
				segundaEleccion = True
			else:
				print("\nIngrese una opcion valida\n")
		except ValueError as e:
			print("\nIngrese solo números\n")

		if segundaEleccion:
			if opcion == 1:
				#Pedimos a usuario la expresion regular
				expresion_regular = input("Expresion regular: ")

				if validarExpresion(expresion_regular) == False:
					break;
				#Pedimos a usuario cadena a evaluar
				cadena = input("Cadena: ")
				postfix = regex_to_postfix(expresion_regular, debug=False)
				nfa = compileNFA(postfix)
				nfa_real = AFN(nfa[0])
				with open('afn.gv', 'w', encoding="utf-8") as f:
					with redirect_stdout(f):
						nfa_real.print_graphviz()
				
				respuesta = match(expresion_regular, cadena)

				if respuesta == True:
					print("La cadena si pertenece")
				else:
					print("La cadena no pertenece")


			elif opcion == 2:
				filename = input("Archivo: ")

				src = Source.from_file(filename)
				src.render('graph.gv', view=True)
			
			elif opcion == 3:
				eleccion = False
				segundaEleccion = False