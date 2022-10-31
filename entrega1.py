from distutils.file_util import move_file
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

#El estado lo representamos con: 
# - Primera tupla donde guardamos la posición del jugador
# - Segunda tupla (Lista de las posiciones actuales de las cajas en el mapa)
# - Tercera tupla lista inicialmente vacia (listaresultado: iremos almacenando y sacando las cajas de la lista a medida que se encuentren en su posición)
# - Cuarta posicion: La cantidad maxima de movimientos

#initial = (
#    (2, 2),
#    ((2, 3), (3, 4), (4, 4), (6, 1), (6, 3), (6, 4), (6, 5)),
#    (),
#    50
#)

#initial = (
#    (2, 3),
#    ((2, 2),),
#    ((3, 5), (4, 1), (5, 4), (6, 3), (7, 4), (6, 6)),
#    50
#)

def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):
    cajas_acomodar = []
    cajas_acomodadas = []
    for x in cajas:
        if x in objetivos:
            cajas_acomodadas.append((x))
        else:
            cajas_acomodar.append((x))
    
    cajas_acomodar = list(cajas_acomodar)
    cajas_acomodadas = list(cajas_acomodadas)

    INITIAL = (
        jugador,
        cajas_acomodar,
        cajas_acomodadas,
        maximos_movimientos
    )

    class Socoban(SearchProblem):
        def cost(self, state, action, state2):
            return 1

        def is_goal(self, state):
            if (len(state[1]) == 0) and (state[3] >= 0):
                return True
            return False

        def actions(self, state):
            pos_jugador, lista_pos_cajas, lista_resultado, movimiento = state
            pos_fila = pos_jugador[0]
            pos_columna = pos_jugador[1]

            lista_acciones = []

            # Compruebo que falten cajas por acomodar y que no haya gastado todos sus movimientos
            if (movimiento > 0) and (len(lista_pos_cajas) > 0):
                # Armo la lista de las posibles acciones

                #   Arriba
                if (pos_fila - 1, pos_columna) not in paredes: # Pregunto si hay un obstaculo
                    if ((pos_fila - 1, pos_columna) in lista_pos_cajas) or ((pos_fila - 1, pos_columna) in lista_resultado): # Pregunto si hay una caja
                        if ((pos_fila - 2, pos_columna) not in paredes) and ((pos_fila - 2, pos_columna) not in lista_pos_cajas) and ((pos_fila - 2, pos_columna) not in lista_resultado): # Pregunto si detras de la caja hay un obstaculo o caja
                            lista_acciones.append(('E', 'Arriba', (pos_fila - 1, pos_columna)))
                    else:
                        lista_acciones.append(('M','Arriba'))

                #   Abajo
                if (pos_fila + 1, pos_columna) not in paredes:
                    if ((pos_fila + 1, pos_columna) in lista_pos_cajas) or ((pos_fila + 1, pos_columna) in lista_resultado):
                        if ((pos_fila + 2, pos_columna) not in paredes) and ((pos_fila + 2, pos_columna) not in lista_pos_cajas) and ((pos_fila + 2, pos_columna) not in lista_resultado):
                            lista_acciones.append(('E', 'Abajo', (pos_fila + 1, pos_columna)))
                    else:
                        lista_acciones.append(('M','Abajo'))

                #   Izquierda
                if (pos_fila, pos_columna - 1) not in paredes:
                    if ((pos_fila, pos_columna - 1) in lista_pos_cajas) or ((pos_fila, pos_columna - 1) in lista_resultado):
                        if ((pos_fila, pos_columna - 2) not in paredes) and ((pos_fila, pos_columna - 2) not in lista_pos_cajas) and ((pos_fila, pos_columna - 2) not in lista_resultado):
                            lista_acciones.append(('E', 'Izquierda', (pos_fila, pos_columna - 1)))
                    else:
                        lista_acciones.append(('M','Izquierda'))

                #   Derecha
                if (pos_fila, pos_columna + 1) not in paredes:
                    if ((pos_fila, pos_columna + 1) in lista_pos_cajas) or ((pos_fila, pos_columna + 1) in lista_resultado):
                        if ((pos_fila, pos_columna + 2) not in paredes) and ((pos_fila, pos_columna + 2) not in lista_pos_cajas) and ((pos_fila, pos_columna + 2) not in lista_resultado):
                            lista_acciones.append(('E', 'Derecha', (pos_fila, pos_columna + 1)))
                    else:
                        lista_acciones.append(('M','Derecha'))
            

            return lista_acciones

        def result(self, state, action):
            player, listacajas, listaresultado, movimientos = state
            state = list(state)
            state[1] = list(state[1])
            state[2] = list(state[2])
            player = list(player)
            listacajas = [list(fila) for fila in listacajas]
            listaresultado = [list(fila) for fila in listaresultado]
            
            if action[1] == 'Izquierda':
                player[1] -= 1
            elif action[1] == 'Derecha':
                player[1] += 1
            elif action[1] == 'Arriba':
                player[0] -= 1
            elif action[1] == 'Abajo':
                player[0] += 1

            if action[0] == 'E':
                aux = action[2]
                aux = list(aux)

                aux2 = action[2]
                aux2 = list(aux2)
                
                if action[1] == 'Izquierda':
                    aux[1] -= 1
                elif action[1] == 'Derecha':
                    aux[1] += 1
                elif action[1] == 'Arriba':
                    aux[0] -= 1
                elif action[1] == 'Abajo':
                    aux[0] += 1

                # Si hay que mover una caja que esta en la posicion correcta, se saca de la listaresultado y se devuelve a la listacajas
                if aux2 in listaresultado:
                    state[2].remove((action[2]))
                    state[1].append((aux))
                elif aux2 in listacajas: 
                    if aux in objetivos: # Si hay que mover una caja hacia la posicion correcta, se saca de la listacajas y se agrega a la listaresultado
                        state[1].remove((action[2]))
                        state[2].append((aux))
                    else: # Si hay que mover la caja a una posicion cualquiera
                        state[1].remove((action[2]))
                        state[1].append((aux))
            
            movimientos -= 1
            state[0] = tuple(player)
            state[1] = tuple([tuple(fila) for fila in state[1]])
            state[2] = tuple([tuple(fila) for fila in state[2]])
            state[3] = movimientos
            state = tuple(state)
            
            return state

        def heuristic(self, state):
            _, lista_cajas, _, _ = state

            return len(lista_cajas)

    #------------------------------------
    #Ejecutar esto para probar el actions:
    #  from entrega1 import Socoban, initial, obstaculos
    #  problem = Socoban(None)
    #  problem.actions(initial)
    #------------------------------------

    problema = Socoban(INITIAL)
    resultado = astar(problema, graph_search=True)
    #resultado = breadth_first(problema)
    #viewer = WebViewer()
    #resultado = breadth_first(Socoban(INITIAL),viewer=viewer)

    #print("Estado meta:")
    #print(resultado.state)

    solucion = []

    #print("Path from initial to goal:")
    for action, state in resultado.path():
        if (action is not None):
            solucion.append(action)

    return solucion

'''
if __name__ == '__main__':
    obstaculos = [
    (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (1, 2), (1, 6), 
    (2, 0), (2, 6), (3, 0), (3, 1), (3, 2), (3, 6), (4, 0), (4, 2), (4, 3), 
    (4, 6), (5, 0), (5, 2), (5, 6), (5, 7), (6, 0), (6, 7), (7, 0), (7, 7), 
    (8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7),
    ]
    objetivo = [
        (2, 1), (3, 5), (4, 1), (5, 4), (6, 3), (7, 4), (6, 6),
    ]
    cajas = [
        ((2, 3), (3, 4), (4, 4), (6, 1), (6, 3), (6, 4), (6, 5))
    ]
    jugador = (2,2)
    maximos_movimientos = 30
    
    secuencia = jugar(obstaculos, cajas, objetivo, jugador, maximos_movimientos)
    print(secuencia)
'''