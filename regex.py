#Alexa Bravo    18831
#Diseño de Lenguajes de Programación 
#Febrero 2023 

#Utilzando Shounting Yard 
def regex_to_postfix(regex):
    precedencia = {'(': 1, '|': 2, '.':3, '+': 4, '?': 4, '*': 4, ';':4, '^':5}
    postfix = []
    operadores = []
    for token in regex:
        if token.isalnum():
            postfix.append(token)
        elif token == '(':
            operadores.append(token)
        elif token == ')':
            while operadores[-1] != '(':
                postfix.append(operadores.pop())
            operadores.pop()  
            # Discartamos los parentesis
        elif token in precedencia:
            while (operadores and operadores[-1] != '('
                   and precedencia.get(token, 3) <= precedencia.get(operadores[-1], 3)):
                postfix.append(operadores.pop())
            operadores.append(token)
    while operadores:
        postfix.append(operadores.pop())

    return ''.join(postfix)