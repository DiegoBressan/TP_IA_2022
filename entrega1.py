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

def jugar(paredes, cajas, objetivos, jugador, maximos_movimientos):
    
    cajas_acomodar = []
    cajas_acomodadas = []
    
    for x in cajas:
        if x in objetivos:
            cajas_acomodadas.append((x))
        else:
            cajas_acomodar.append((x))

    cajas_acomodar = tuple([tuple(fila) for fila in cajas_acomodar])
    cajas_acomodadas = tuple([tuple(fila) for fila in cajas_acomodadas])

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
                            if (pos_fila - 2, pos_columna) in objetivos: # Pregunta si la posicion es un objetivo
                                lista_acciones.append(('E', 'arriba', (pos_fila - 1, pos_columna)))
                            else:
                                if (pos_fila - 3, pos_columna) not in paredes:
                                    lista_acciones.append(('E', 'arriba', (pos_fila - 1, pos_columna)))
                                else:
                                    if ((pos_fila - 2, pos_columna - 1) not in lista_pos_cajas and (pos_fila - 2, pos_columna - 1) not in lista_resultado) and ((pos_fila - 2, pos_columna + 1) not in lista_pos_cajas and (pos_fila - 2, pos_columna + 1) not in lista_resultado):
                                        # Pergunta que no tenga paredes, para que no quede en una esquina 
                                        lista_acciones.append(('E', 'arriba', (pos_fila - 1, pos_columna)))
                    else:
                        lista_acciones.append(('M','arriba'))

                #   Abajo
                if (pos_fila + 1, pos_columna) not in paredes:
                    if ((pos_fila + 1, pos_columna) in lista_pos_cajas) or ((pos_fila + 1, pos_columna) in lista_resultado):
                        if ((pos_fila + 2, pos_columna) not in paredes) and ((pos_fila + 2, pos_columna) not in lista_pos_cajas) and ((pos_fila + 2, pos_columna) not in lista_resultado):
                            if (pos_fila + 2, pos_columna) in objetivos: # Pregunta si la posicion es un objetivo
                                lista_acciones.append(('E', 'abajo', (pos_fila + 1, pos_columna)))
                            else:
                                if (pos_fila + 3, pos_columna) not in paredes:
                                    lista_acciones.append(('E', 'abajo', (pos_fila + 1, pos_columna)))
                                else:
                                    if ((pos_fila + 2, pos_columna - 1) not in lista_pos_cajas and (pos_fila + 2, pos_columna - 1) not in lista_resultado) and ((pos_fila + 2, pos_columna + 1) not in lista_pos_cajas and (pos_fila + 2, pos_columna + 1) not in lista_resultado):
                                        # Pergunta que no tenga paredes, para que no quede en una esquina 
                                        lista_acciones.append(('E', 'abajo', (pos_fila + 1, pos_columna)))
                    else:
                        lista_acciones.append(('M','abajo'))

                #   Izquierda
                if (pos_fila, pos_columna - 1) not in paredes:
                    if ((pos_fila, pos_columna - 1) in lista_pos_cajas) or ((pos_fila, pos_columna - 1) in lista_resultado):
                        if ((pos_fila, pos_columna - 2) not in paredes) and ((pos_fila, pos_columna - 2) not in lista_pos_cajas) and ((pos_fila, pos_columna - 2) not in lista_resultado):
                            if (pos_fila, pos_columna - 2) in objetivos: # Pregunta si la posicion es un objetivo
                                    lista_acciones.append(('E', 'izquierda', (pos_fila, pos_columna - 1)))
                            else:
                                if (pos_fila, pos_columna - 3) not in paredes:
                                    lista_acciones.append(('E', 'izquierda', (pos_fila, pos_columna - 1)))
                                else:
                                    if ((pos_fila - 1, pos_columna - 2) not in lista_pos_cajas and (pos_fila - 1, pos_columna - 2) not in lista_resultado) and ((pos_fila + 1, pos_columna - 2) not in lista_pos_cajas and (pos_fila + 1, pos_columna - 2) not in lista_resultado):
                                        # Pergunta que no tenga paredes, para que no quede en una esquina 
                                        lista_acciones.append(('E', 'izquierda', (pos_fila, pos_columna - 1)))
                    else:
                        lista_acciones.append(('M','izquierda'))

                #   Derecha
                if (pos_fila, pos_columna + 1) not in paredes:
                    if ((pos_fila, pos_columna + 1) in lista_pos_cajas) or ((pos_fila, pos_columna + 1) in lista_resultado):
                        if ((pos_fila, pos_columna + 2) not in paredes) and ((pos_fila, pos_columna + 2) not in lista_pos_cajas) and ((pos_fila, pos_columna + 2) not in lista_resultado):
                            if (pos_fila, pos_columna + 2) in objetivos: # Pregunta si la posicion es un objetivo
                                    lista_acciones.append(('E', 'derecha', (pos_fila, pos_columna + 1)))
                            else:
                                if (pos_fila, pos_columna + 3) not in paredes:
                                    lista_acciones.append(('E', 'derecha', (pos_fila, pos_columna + 1)))
                                else:
                                    if ((pos_fila - 1, pos_columna + 2) not in lista_pos_cajas and (pos_fila - 1, pos_columna + 2) not in lista_resultado) and ((pos_fila + 1, pos_columna + 2) not in lista_pos_cajas and (pos_fila + 1, pos_columna + 2) not in lista_resultado):
                                        # Pergunta que no tenga paredes, para que no quede en una esquina 
                                        lista_acciones.append(('E', 'derecha', (pos_fila, pos_columna + 1)))
                    else:
                        lista_acciones.append(('M','derecha'))            

            return lista_acciones

        def result(self, state, action):
            player, listacajas, listaresultado, movimientos = state
            state = list(state)
            state[1] = list(state[1])
            state[2] = list(state[2])
            player = list(player)
            listacajas = [list(fila) for fila in listacajas]
            listaresultado = [list(fila) for fila in listaresultado]
            listaobjetivos = [list(fila) for fila in objetivos]
            
            if action[1] == 'izquierda':
                player[1] -= 1
            elif action[1] == 'derecha':
                player[1] += 1
            elif action[1] == 'arriba':
                player[0] -= 1
            elif action[1] == 'abajo':
                player[0] += 1

            if action[0] == 'E':
                aux = action[2]
                aux = list(aux)

                aux2 = action[2]
                aux2 = list(aux2)
                
                if action[1] == 'izquierda':
                    aux[1] -= 1
                elif action[1] == 'derecha':
                    aux[1] += 1
                elif action[1] == 'arriba':
                    aux[0] -= 1
                elif action[1] == 'abajo':
                    aux[0] += 1

                # Si hay que mover una caja que esta en la posicion correcta, se saca de la listaresultado y se devuelve a la listacajas
                if aux2 in listaresultado:
                    state[2].remove((action[2]))
                    state[1].append((aux))
                elif aux2 in listacajas: 
                    if aux in listaobjetivos: # Si hay que mover una caja hacia la posicion correcta, se saca de la listacajas y se agrega a la listaresultado
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

    #----------------------------------------------------
    problema = Socoban(INITIAL)
    resultado = astar(problema, graph_search=True)

    solucion = []
    for action, state in resultado.path():
        if (action is not None):
            solucion.append(action[1])

    return solucion
    #----------------------------------------------------