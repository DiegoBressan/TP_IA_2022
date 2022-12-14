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

    # Funcion que utilizamos en la ultima restriccion, que guarda las posiciones de la grilla
    grilla = []
    for x in range(filas):
        for y in range(columnas):
            grilla.append((x, y))

    def Paredes_con_Paredes(variables, values): # Que no hayan paredes en la misma posicion
        p1, p2 = values
        if p1 != p2:
            return True # Las paredes no estan en la misma posicion
        else:
            return False # Las paredes estan en la misma posicion

    for p1, p2 in combinations(lista_paredes, 2):
        restricciones.append(((p1, p2), Paredes_con_Paredes))
    
    def Cajas_con_cajas(variables, values): # Que no hayan cajas en la misma posicion
        c1, c2 = values
        if c1 != c2:
            return True # Las cajas no estan en la misma posicion
        else:
            return False # Las cajas estan en la misma posicion

    for c1, c2 in combinations(lista_cajas, 2):
        restricciones.append(((c1, c2), Cajas_con_cajas))

    def Objetivos_con_objetivos(variables, values): # Que no hayan objetivos en la misma posicion
        o1, o2 = values
        if o1 != o2:
            return True # Los objetivos no estan en la misma posicion
        else:
            return False # Los objetivos estan en la misma posicion

    for o1, o2 in combinations(lista_objetivos, 2):
        restricciones.append(((o1, o2), Objetivos_con_objetivos))

    def Cajas_con_paredes(variables, values): # Que no hayan cajas en la misma posicion que las paredes
        c, p = values
        if c == p:
            return False # Estan en la misma posicion
        return True # No estan en la misma posicion

    for cajita in lista_cajas:
        for paredsita in lista_paredes:
            restricciones.append(((cajita, paredsita), Cajas_con_paredes))

    def Paredes_con_objetivos(variables, values): # Que no hayan Paredes en los objetivos
        p, o = values
        if p == o:
            return False # Estan en la misma posicion
        return True # No estan en la misma posicion

    for objetivito in lista_objetivos:
        for paredsita in lista_paredes:
            restricciones.append(((paredsita, objetivito), Paredes_con_objetivos))

    def Player_con_CajasParedes(variables, values): # Que el player no este en una pared o una caja
        p, cp = values
        if p == cp:
            return False # Estan en la misma posicion
        return True # No estan en la misma posicion

    for c in lista_cajas:
        restricciones.append((('Persona' ,c), Player_con_CajasParedes))
    
    for pa in lista_paredes:
        restricciones.append((('Persona' ,pa), Player_con_CajasParedes))

    def Cajas_en_Objetivos(variables, values):
        for c in lista_cajas:
            if c not in lista_objetivos:
                return True # Si encuentra una caja que no este en los objetivos, entonces no estan todas las cajas en los objetivos
        return False # Si no encuentra una caja que no este en objetivo, entonces todas las cajas estan en objetivos

    restricciones.append((variables, Cajas_en_Objetivos))

    def Caja_no_paredes_adyacentes(variables, values): # Que las cajas no tengan paredes adyacentes si estan en el borde, y si no estan en el borde pueden tener 1 o menos
        caja = values[0]
        fila_caja, columna_caja = caja
        c = 0

        posiciones_adyacentes = []
        if (fila_caja + 1, columna_caja) in grilla:
            posiciones_adyacentes.append((fila_caja + 1, columna_caja))
        if (fila_caja - 1, columna_caja) in grilla:
            posiciones_adyacentes.append((fila_caja - 1, columna_caja))
        if (fila_caja, columna_caja + 1) in grilla:
            posiciones_adyacentes.append((fila_caja, columna_caja + 1))
        if (fila_caja, columna_caja - 1) in grilla:
            posiciones_adyacentes.append((fila_caja, columna_caja - 1))

        for posicion in values:
            if posicion in posiciones_adyacentes:
                c += 1

        if (fila_caja == 0) or (fila_caja == filas) or (columna_caja == 0) or (columna_caja == columnas): # Si la caja esta en el borde
            if c == 0: # Si NO tiene ninguna pared adyacente
                return True
        else: # Si NO est?? en el borde
            if c <= 1: # Si tiene M??NIMO 1 pared adyacente
                return True
        
        return False

    if len(lista_paredes) > 1: # Pregunto cuantas paredes hay, y si hay mas de una, tomo por cada caja, combinaciones de 2 predes.
        for c in lista_cajas:    
            for p1, p2 in combinations(lista_paredes, 2):          
                restricciones.append(((c, p1, p2), Caja_no_paredes_adyacentes))
    else: # Sino , por cada caja, consulto por la unica pared
        p1 = lista_paredes[0]
        for c in lista_cajas: 
            restricciones.append(((c, p1), Caja_no_paredes_adyacentes))

    
    #--------------------------------------------------------
    problema = CspProblem(variables, dominios, restricciones)
    result = backtrack(problema, inference=False, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE,)
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
    
    return (solucion_pared, solucion_caja, solucion_objetivo, solucion_player)
    #--------------------------------------------------------
