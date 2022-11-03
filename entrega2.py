from itertools import combinations
from simpleai.search import (
    CspProblem,
    backtrack,
    LEAST_CONSTRAINING_VALUE,
    min_conflicts, 
    MOST_CONSTRAINED_VARIABLE
)

def armar_mapa(filas, columnas, cantidad_paredes, cantidad_cajas_objetivos):
    paredes = cantidad_paredes
    cajas = cantidad_cajas_objetivos
    objetivos = cantidad_cajas_objetivos

    #filas = 3
    #columnas = 3
    #paredes = 1
    #cajas = 1
    #objetivos = 1

    # Consideramos como variables a las paredes cajas y objetivos que debemos colocar
    variables = []
    lista_paredes = []
    lista_cajas = []
    lista_objetivos = []

    # Realizamos 3 for para cargar la cantidad necesaria de paredes, cajas y objetivos que requiera el problema
    for x in range(1, paredes+1):
        variables.append(f'Pared{x}')
        lista_paredes.append(f'Pared{x}')

    for x in range(1, cajas+1):
        variables.append(f'Caja{x}')
        lista_cajas.append(f'Caja{x}')

    for x in range(1, objetivos+1):
        variables.append(f'Objetivo{x}')
        lista_objetivos.append(f'Objetivo{x}')

    variables.append('Persona')

    # Consideramos como dominios a las coordenadas a las cuales pueden ser asignadas las paredes, cajas y objetivos
    dominios = {}
    esquinas = [(0, 0), (0, columnas-1), (filas-1, 0), (filas-1, columnas-1)]

    # A cada variable le cargamos en el dominio todas las coordenadas que pueden elegir
    for variable in variables:
        if variable in lista_cajas:
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

    # Genero la lista restricciones y las restricciones
    restricciones = []

    def Paredes_con_Paredes(pared, values): # Que no hayan paredes en la misma posicion
        if values[pared[0]] != values[pared[1]]:
            return True # Las paredes no estan en la misma posicion
        else:
            return False # Las paredes estan en la misma posicion

    for p1, p2 in combinations(lista_paredes, 2):
        restricciones.append(((p1, p2), Paredes_con_Paredes))
    
    def Cajas_con_cajas(caja, values): # Que no hayan cajas en la misma posicion
        if values[caja[0]] != values[caja[1]]:
            return True # Las cajas no estan en la misma posicion
        else:
            return False # Las cajas estan en la misma posicion

    for c1, c2 in combinations(lista_cajas, 2):
        restricciones.append(((c1, c2), Cajas_con_cajas))

    def Objetivos_con_objetivos(objetivo, values): # Que no hayan objetivos en la misma posicion
        if values[objetivo[0]] != values[objetivo[1]]:
            return True # Los objetivos no estan en la misma posicion
        else:
            return False # Los objetivos estan en la misma posicion

    for o1, o2 in combinations(lista_objetivos, 2):
        restricciones.append(((o1, o2), Objetivos_con_objetivos))

    def Cajas_con_paredes(caja_pared, values): # Que no hayan cajas en la misma posicion que las paredes
        if values[caja_pared[0]] == values[caja_pared[1]]:
            return False # Estan en la misma posicion
        return True # No estan en la misma posicion

    for cajita in lista_cajas:
        for paredsita in lista_paredes:
            restricciones.append(((cajita, paredsita), Cajas_con_paredes))

    def Paredes_con_objetivos(pared_objetivo, values): # Que no hayan Paredes en los objetivos
        if values[pared_objetivo[0]] == values[pared_objetivo[1]]:
            return False # Estan en la misma posicion
        return True # No estan en la misma posicion

    for objetivito in lista_objetivos:
        for paredsita in lista_paredes:
            restricciones.append(((paredsita, objetivito), Paredes_con_objetivos))

    def Player_con_CajasParedes(caja_pared, values): # Que el player no este en una pared o una caja
        if values['Persona'] == values[caja_pared]:
            return False # Estan en la misma posicion
        return True # No estan en la misma posicion

    for c in lista_cajas:
        restricciones.append((c, Player_con_CajasParedes))

    def Cajas_en_Objetivos(cajas_objetivos, values):
        for c in cajas_objetivos[0]:
            ban = True
            for o in cajas_objetivos[1]:
                if values[c] == values[o]:
                    ban = False
                    break
            if ban:
                return True # Si encuentra una caja que no este en los objetivos, entonces no estan todas las cajas en los objetivos
        return False # Si no encuentra una caja que no este en objetivo, entonces todas las cajas estan en objetivos

    restricciones.append(((lista_cajas, lista_objetivos), Cajas_en_Objetivos))

    def Caja_no_paredes_adyacentes(caja_paredes, values):
        cont = 0
        if values[caja_paredes[0]][0] == 0:
            cont += 1
        if values[caja_paredes[0]][1] == 0:
            cont += 1
        if values[caja_paredes[0]][0] == filas-1:
            cont += 1
        if values[caja_paredes[0]][1] == columnas-1:
            cont += 1
        
        # Pregunto si la caja tiene pegada una de las paredes internas
        for pared in caja_paredes[1]:
            aux = (values[caja_paredes[0]][0] - 1, values[caja_paredes[0]][1])
            if aux == values[pared]:
                cont += 1

            aux = (values[caja_paredes[0]][0] + 1, values[caja_paredes[0]][1])
            if aux == values[pared]:
                cont += 1

            aux = (values[caja_paredes[0]][0], values[caja_paredes[0]][1] - 1)
            if aux == values[pared]:
                cont += 1
                
            aux = (values[caja_paredes[0]][0], values[caja_paredes[0]][1] + 1)
            if aux == values[pared]:
                cont += 1

        if cont >= 2:
            return False # Si encuentra una caja que tenga 2 o mas paredes, retorna false
        
        return True # Si no encontro caja con 2 o mas paredes, retorna True

    for c in lista_cajas:
        restricciones.append(((c, lista_paredes), Caja_no_paredes_adyacentes))

    #--------------------------------------------------------
    problema = CspProblem(variables, dominios, restricciones)
    result = backtrack(problema)
    #print('Resultado: ')
    #print(result)
    #result = list(result)
    result = tuple([tuple(fila) for fila in result])
    solucion_pared = []
    solucion_caja = []
    solucion_objetivo = []
    solucion_player = result['Persona']
    for p in lista_paredes:
        solucion_pared.append((result[p]))
    
    for c in lista_cajas:
        solucion_caja.append((result[c]))
    
    for o in lista_objetivos:
        solucion_objetivo.append((result[o]))
    
    solucion = (
        solucion_pared,
        solucion_caja,
        solucion_objetivo,
        solucion_player
    )
    solucion = tuple(solucion)
    return solucion
    #--------------------------------------------------------

    #print(variables)
    #print(dominios)
    #print(lista_grilla)
    #print(nuevalista)
