#Alexa Bravo    18831
#Diseño de Lenguajes de Programación 
#Febrero 2023 

from afn import AFN, EstadoAFN

#Nodos de los arboles
class Nodo:
	
    #Construcción de Thompson
	def algoritmoThompson(self):
		raise NotImplementedError
		
    #Convertir el nodo en un AFN
	def conversionAFN(self, estadoAceptacion_id = 1):
		(initial, estadoAceptacion) = self.thompson()
		estadoAceptacion.estadoAceptacion = estadoAceptacion_id
		return AFN(initial)


#Nodo para los simbolos que se ingresan 
class Simbolo(Nodo):

	def __init__(self, symbol):
		super().__init__()
		self.symbol = symbol

	def thompson(self):
		estadoInicial = EstadoAFN()
		estadoAceptación = EstadoAFN()
		estadoInicial.add_transition(self.symbol, estadoAceptación)
		return (estadoInicial, estadoAceptación)

	def __str__(self):
		return 'Simbolo({})'.format(repr(self.symbol))

#Nodo para Kleen 
class Kleene(Nodo):

	def __init__(self, operand):
		super().__init__()
		self.operand = operand

	def thompson(self, estadoInicial, estadoAceptacion):

		estadoInicial.add_transition(None, estadoAceptacion)
		estadoAceptacion.add_transition(None, estadoInicial)

		return (estadoInicial, estadoAceptacion)

	def __str__(self):
		return 'Kleene({})'.format(repr(self.operand))



#Nodo para ? ingresados
class Interrogacion(Nodo):

	def __init__(self, operand):
		super().__init__()
		self.operand = operand

	def thompson(self, estadoInicial, estadoAceptacion):

		estadoAceptacion.add_transition(None, estadoAceptacion)

		return (estadoInicial, estadoAceptacion)

	def __str__(self):
		return 'Interrogacion({})'.format(repr(self.operand))

#Nodo para ! ngresados
class Or(Nodo):

	def __init__(self, *operands):

		super().__init__()

		if len(operands) < 2:
			raise ValueError('Se necesitan dos nodos hijos')

		self.operands = ()
		for nodo in operands:
			#Si hay otro OR en un nodo hijo, se agregan
			if isinstance(nodo, Or):
				self.operands += nodo.operands
			else:
				self.operands += (nodo,)

	def thompson(self):
		estadoInicial = EstadoAFN()
		estadoAceptacion = EstadoAFN()

		for nodo in self.operands:
			if nodo == "|":
				pass
			else:
				#Se agregan las dos transiciones 
				(initial_new, accept_new) = (nodo[0], nodo[1])
				estadoInicial.add_transition(None, initial_new)
				accept_new.add_transition(None, estadoAceptacion)
			
		return (estadoInicial, estadoAceptacion)

	def __str__(self):
		return 'OR ({})'.format(', '.join(repr(o) for o in self.operands))
	
#Nodo para el signo + ingresado
class Mas(Nodo):

	def __init__(self, operand):
		super().__init__()
		self.operand = operand

	def thompson(self, estadoInicial, estadoAceptacion):

		estadoAceptacion.add_transition(None, estadoInicial)

		return (estadoInicial, estadoAceptacion)

	def __str__(self):
		return 'Mas({})'.format(repr(self.operand))
	
#Nodo de concatenación
class Concatenacion(Nodo):

	def __init__(self, *operands):

		super().__init__()

		if len(operands) < 2:
			raise ValueError("Se necesitan dos nodos para concatenarlos")

		self.operands = ()

		for nodo in operands:
			if isinstance(nodo, Concatenacion):
				self.operands += nodo.operands
			else:
				self.operands += (nodo )

	def thompson(self):

		(estadoInicial, estadoAceptacion) = self.operands[1]

		for i in range(1, len(self.operands)):
			(nxt_initial, nxt_accept) = self.operands[i]
			accept.add_transition(None, nxt_initial)
			accept = nxt_accept

		return (estadoInicial, estadoAceptacion)

	def __str__(self):
		return 'Concatenacion ({})'.format(', '.join(repr(o) for o in self.operands))