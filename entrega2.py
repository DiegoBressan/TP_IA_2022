from itertools import combinations
from simpleai.search import (
    CspProblem,
    backtrack,
    LEAST_CONSTRAINING_VALUE,
    min_conflicts, 
    MOST_CONSTRAINED_VARIABLE
)

paredes = 3
cajas = 2
objetivos = 2

filas = 3
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


def Devolver_listas(variable, valor):
    
    lista_paredes = []
    lista_cajas = []
    lista_objetivos = []

    for indice, v in enumerate(variable):
        if v[0] == 'Pared':
            lista_paredes.append(valor[indice])
        elif v[0] == 'Cajas':
            lista_cajas.append(valor[indice])
        elif v[0] == 'Objetivos':
            lista_objetivos.append(valor[indice])
        elif v[0] == 'Persona':
            player = valor[indice]

    return (lista_paredes, lista_cajas, lista_objetivos, player)

def Paredes_con_Paredes(variables, values): # Que no hayan paredes en la misma posicion
    
    paredes, _, _, _ = Devolver_listas(variables, values)

    if len(paredes) == len(set(paredes)):
        return True # Todos los valores de paredes son diferentes
    else:
        return False # Hay 2 valores que son iguales, se viola la restriccion

restricciones.append((variables, Paredes_con_Paredes))

def Cajas_con_cajas(variables, values): # Que no hayan cajas en la misma posicion

    _, cajas, _, _ = Devolver_listas(variables, values)

    if len(cajas) == len(set(cajas)):
        return True # Todos los valores de cajas son diferentes
    else:
        return False # Hay 2 valores que son iguales, se viola la restriccion

restricciones.append((variables, Cajas_con_cajas))

def Objetivos_con_objetivos(variables, values): # Que no hayan objetivos en la misma posicion

    _, _, objetivos, _ = Devolver_listas(variables, values)

    if len(objetivos) == len(set(objetivos)):
        return True # Todos los valores de objetivos son diferentes
    else:
        return False # Hay 2 valores que son iguales, se viola la restriccion

restricciones.append((variables, Objetivos_con_objetivos))

def Cajas_con_paredes(variables, values): # Que no hayan cajas en la misma posicion que las paredes

    paredes, cajas, _, _ = Devolver_listas(variables, values)

    for caja in cajas:
        if caja in paredes:
            return False # Hay una caja en una pared, se viola la restriccion

    return True # No hay cajas en las paredes

restricciones.append((variables, Cajas_con_paredes))

def Paredes_con_objetivos(variables, values): # Que no hayan Paredes en los objetivos

    paredes, _, objetivos, _ = Devolver_listas(variables, values)

    for objetivo in objetivos:
        if objetivo in paredes:
            return False # Hay un objetivo en una pared, se viola la restriccion
    
    return True # No hay objetivos en las paredes

restricciones.append((variables, Paredes_con_objetivos))

def Player_con_CajasParedes(variables, values): # Que el player no este en una pared o una caja

    paredes, cajas, _, player = Devolver_listas(variables, values)

    if (player in paredes) or (player in cajas):
        return False # El jugador esta en la posicion de una caja o una pared, se viola la restriccion

    return True # El jugador no se encuentra en la posicion de una pared o caja

restricciones.append((variables, Player_con_CajasParedes))

def Cajas_en_Objetivos(variables, values):
    _, cajas, objetivos, _ = Devolver_listas(variables, values)
    for c in cajas:
        if c not in objetivos:
            return True # Si encuentra una caja que no este en objetivo, entonces no todas las cajas estan en objetivos
    return False # Si no encuentra una caja que no este en objetivo, entonces todas las cajas estan en objetivos

restricciones.append((variables, Cajas_en_Objetivos))

def Caja_no_paredes_adyacentes(variables, values):
    paredes, cajas, objetivos, _ = Devolver_listas(variables, values)
    for c in cajas:
        cont = 0

        # Pregunto si la caja esta pegada a una de las paredes externas 
        if c[0] == 0:
            cont += 1
        if c[1] == 0:
            cont += 1
        if c[0] == filas:
            cont += 1
        if c[1] == columnas:
            cont += 1
        
        # Pregunto si la caja tiene pegada una de las paredes internas
        aux = (c[0] - 1, c[1])
        if aux in paredes:
            cont += 1

        aux = (c[0] + 1, c[1])
        if aux in paredes:
            cont += 1

        aux = (c[0], c[1] - 1)
        if aux in paredes:
            cont += 1
        
        aux = (c[0], c[1] + 1)
        if aux in paredes:
            cont += 1

        if cont >= 2:
            return False # Si encuentra una caja que tenga 2 o mas paredes, retorna false

    return True # Si no encontro caja con 2 o mas paredes, retorna True

restricciones.append((variables, Caja_no_paredes_adyacentes))

#--------------------------------------------------------
problema = CspProblem(variables, dominios, restricciones)
result = backtrack(problema)
print('Resultado: ')
print(result)
#--------------------------------------------------------

#print(variables)
#print(dominios)
#print(lista_grilla)
#print(nuevalista)