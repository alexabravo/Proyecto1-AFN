#Alexa Bravo    18831
#Diseño de Lenguajes de Programación 
#Febrero 2023 

class Automata:
	
	def __init__(self, estadoInicial):
		self.estadoInicial = estadoInicial
		self.num_states = self.assign_number_state(self.estadoInicial, 0)

	def assign_number_state(self, state, nxt_num):
		if state.number is None:
			state.number = nxt_num
			nxt_num += 1
			for (symbol, target) in state.all_transitions():
				nxt_num = self.assign_number_state(target, nxt_num)
		return nxt_num

	def print_graphviz(self):
	#Graficas

		print('digraph {} {{'.format(type(self).__name__))
		print('    edge [dir="back"];')
		print('    rankdir = RL;')
		print('    I [style = invis];')

		print('    I -> S{};'.format(self.estadoInicial.number))
		
		self.estadoInicial._print_graphviz(set())

		print('}')


class EstadoAutomata:

	def __init__(self, accept=None):
		self.accept = accept
		self.transitions = {}
		self.number = None

	def _ensure_not_numbered(self):

		if self.number is not None:
			raise ValueError('Estado previamente numerado')

	def all_transitions():

		raise NotImplementedError

	def add_transition(self, symbol, to):

		raise NotImplementedError


	def _print_graphviz(self, seen):
		if self in seen:
			return
		seen.add(self)

		if self.accept:
			subscript = '{},{}'.format(self.number, self.accept)
		else:
			subscript = self.number

		print('    S{} [label = <s<sub>{}</sub>>, shape = circle'.format(self.number, subscript),
			  end='')

		if self.accept:
			print(', peripheries = 2', end='')
		print('];')

		for (symbol, target) in self.all_transitions():
			target._print_graphviz(seen)
			if symbol is None:
				label = '\u03b5' 
			else:
				label = repr(symbol).replace('\\', '\\\\')  
			print('    S{} -> S{} [label = "{}"];'.format(self.number, target.number, label))
			
class AFN(Automata):

	def __init__(self, estadoInicial):
		super().__init__(estadoInicial)

class EstadoAFN(EstadoAutomata):


	def __init__(self, accept=None):
		super().__init__(accept)

	def all_transitions(self):

		transitions = set()
		for symbol, targets in self.transitions.items():

			transitions |= {(symbol, target) for target in targets}
		return transitions

	def add_transition(self, symbol, state):


		self._ensure_not_numbered()

		try:
			self.transitions[symbol].add(state)
		except KeyError:
			self.transitions[symbol] = {state}

	def e_closure(self):

		ephsilon = {self}
		stack = [self]
		while stack:
			state = stack.pop()
			for target in state.transitions.get(None, set()):
				if target not in ephsilon:
					ephsilon.add(target)
					stack.append(target)

		self.inmutable_ephsilon = frozenset(ephsilon)
		return self.inmutable_ephsilon