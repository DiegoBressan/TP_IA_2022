from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar
)

from simpleai.search.viewers import WebViewer, BaseViewer

# Consideramos como variables a las paredes cajas y objetivos que debemos colocar
variables = []
# Realizamos 3 for para cargar la cantidad necesaria de paredes, cajas y objetivos que requiera el problema
for x in range(1, paredes):
    variables.append(('Pared', x))

for x in range(1, cajas):
    variables.append(('Cajas', x))

for x in range(1, objetivos):
    variables.append(('Objetivos', x))

variables.append(('Persona', 0))

variables = tuple(variables)

# Consideramos como dominios a las coordenadas a las cuales pueden ser asignadas las paredes, cajas y objetivos
dominios = {}
esquinas = ((0,0),(0, columnas),(filas,0),(filas, columnas))
# A cada variable le cargamos en el dominio todas las coordenadas que pueden elegir
for x in variables:
    for f in range(0, filas):
        for c in range(9, columnas):
            if (f, c) in esquinas:
                if x[0] != 'Cajas':
                    dominios[x] = [( f, c)]
            else:
                dominios[x] = [( f, c)]

dominios = tuple(dominios)

restricciones = ()