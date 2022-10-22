from itertools import combinations
from simpleai.search import (
    CspProblem,
    backtrack,
    LEAST_CONSTRAINING_VALUE,
    min_conflicts, 
    MOST_CONSTRAINED_VARIABLE
)

paredes = 2
cajas = 2
objetivos = 2

filas = 4
columnas = 4

# Consideramos como variables a las paredes cajas y objetivos que debemos colocar
variables = []
# Realizamos 3 for para cargar la cantidad necesaria de paredes, cajas y objetivos que requiera el problema
for x in range(paredes):
    variables.append(('Pared', x))

for x in range(cajas):
    variables.append(('Cajas', x))

for x in range(objetivos):
    variables.append(('Objetivos', x))

variables.append(('Persona', 0))

# Consideramos como dominios a las coordenadas a las cuales pueden ser asignadas las paredes, cajas y objetivos
dominios = {}
esquinas = [(0, 0), (0, columnas-1), (filas-1, 0), (filas-1, columnas-1)]

# A cada variable le cargamos en el dominio todas las coordenadas que pueden elegir

for variable in variables:
    if variable[0] == 'Cajas':
        
        lista_grilla1 = []
        for x in range(filas):
            for y in range(columnas):
                lista_grilla1.append((x, y))

        # Verifico que en la lista no esten las esquinas y si las hay las saco
        # Para restringir del dominio que las cajas no puedan colocarse en las esquinas
        for esquina in esquinas:
            for coordenada in lista_grilla1:
                if esquina == coordenada:
                    lista_grilla1.remove(coordenada)

        dominios[variable] = lista_grilla1
    else:
        
        lista_grilla2 = []
        for x in range(filas):
            for y in range(columnas):
                lista_grilla2.append((x, y))

        dominios[variable] = lista_grilla2

restricciones = []


#def Devolver_listas(valor):
    
#    lista_paredes = []
#    lista_cajas = []
#    lista_objetivos = []
#    player = []
#    for variable in valor:
#        if variable[0] == 'P':
#            lista_paredes.append(variable)
#        elif variable[0] == 'C':
#            lista_cajas.append(variable)
#        elif variable[0] == 'O':
#            lista_objetivos.append(variable)
#        else:
#            player.append(variable)

#    return (lista_paredes, lista_cajas, lista_objetivos, player)

def Paredes_con_Paredes(variables, values): # Que no hayan paredes en la misma posicion
    
    paredes, _, _, _ = Devolver_listas(values)

    if len(paredes) == len(set(paredes)):
        return False # Todos los valores de paredes son diferentes
    else:
        return True # Hay 2 valores que son iguales, se viola la restriccion

restricciones.append((variables, Paredes_con_Paredes))

def Cajas_con_cajas(variables, values): # Que no hayan cajas en la misma posicion

    _, cajas, _, _ = Devolver_listas(values)

    if len(cajas) == len(set(cajas)):
        return False # Todos los valores de cajas son diferentes
    else:
        return True # Hay 2 valores que son iguales, se viola la restriccion

restricciones.append((variables, Cajas_con_cajas))

def Cajas_con_paredes(variables, values): # Que no hayan cajas en la misma posicion que las paredes

    paredes, cajas, _, _ = Devolver_listas(values)

    for caja in cajas:
        if caja in paredes:
            return True # Hay una caja en una pared, se viola la restriccion

    return False # No hay cajas en las paredes

restricciones.append((variables, Cajas_con_paredes))

def Paredes_con_objetivos(variables, values): # Que no hayan Paredes en los objetivos

    paredes, _, objetivos, _ = Devolver_listas(values)

    for objetivo in objetivos:
        if objetivo in paredes:
            return True # Hay un objetivo en una pared, se viola la restriccion
    
    return False # No hay objetivos en las paredes

restricciones.append((variables, Paredes_con_objetivos))

def Player_con_CajasParedes(variables, values): # Que el player no este en una pared o una caja

    paredes, cajas, _, player = Devolver_listas(values)

    for jugador in player:
        if (jugador in paredes) or (jugador in cajas):
            return True # El jugador esta en la posicion de una caja o una pared, se viola la restriccion

    return False # El jugador no se encuentra en la posicion de una pared o caja

restricciones.append((variables, Player_con_CajasParedes))


#--------------------------------------------------------
#problema = CspProblem(variables, dominios, restricciones)
#result = backtrack(problema)
#print('Resultado: ')
#print(result)
#--------------------------------------------------------

#print(variables)
print(dominios)
#print(lista_grilla)
#print(nuevalista)