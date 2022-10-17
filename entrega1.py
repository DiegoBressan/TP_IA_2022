from ctypes import cdll
from simpleai.search import (
    SearchProblem,
    breadth_first,
    depth_first,
    uniform_cost,
    limited_depth_first,
    iterative_limited_depth_first,
    astar
)

#El estado lo representamos con: 
# - Primera tupla donde guardamos la posición del jugador
# - Segunda tupla (Lista de las posiciones actuales de las cajas en el mapa)
# - Tercera tupla lista inicialmente vacia (iremos almacenando y sacando las cajas de la lista a medida que se encuentren en su posición)
# - La cantidad maxima de mivimientos

initial = (

    (4, 4),
    ((2, 3), (3, 4), (6, 1), (6, 3), (6, 4), (6, 5)),
    ((5, 4),),
    50

)

obstaculos = (
(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (1, 2), (1, 6), 
(2, 0), (2, 6), (3, 0), (3, 1), (3, 2), (3, 6), (4, 0), (4, 2), (4, 3), 
(4, 6), (5, 0), (5, 2), (5, 6), (5, 7), (6, 0), (6, 7), (7, 0), (7, 7), 
(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7),
)

objetivos = (
    (2, 1), (3, 5), (4, 1), (5, 4), (6, 3), (7, 4), (6, 6),
)

from simpleai.search.viewers import WebViewer, BaseViewer

class Socoban(SearchProblem):

    def cost(self, state, action, state2):
        return 1

    def is_goal(self, state):
        if (state[1] == () and state[3] >= 0):
            return True 

    def actions(self, state):
        pos_jugador, lista_pos_cajas, lista_resultado, max_mov = state
        pos_fila = pos_jugador[0]
        pos_columna = pos_jugador[1]

        lista_acciones = []

        # Armo la lista de las posibles acciones

        #   Arriba
        if (pos_fila - 1, pos_columna) not in obstaculos: # Pregunto si hay un obstaculo
            if ((pos_fila - 1, pos_columna) in lista_pos_cajas) or ((pos_fila - 1, pos_columna) in lista_resultado): # Pregunto si hay una caja
                if ((pos_fila - 2, pos_columna) not in obstaculos) and ((pos_fila - 2, pos_columna) not in lista_pos_cajas) and ((pos_fila - 2, pos_columna) not in lista_resultado): # Pregunto si detras de la caja hay un obstaculo o caja
                    lista_acciones.append(('E', 'Arriba', (pos_fila - 1, pos_columna)))
            else:
                lista_acciones.append(('M','Arriba'))

        #   Abajo
        if (pos_fila + 1, pos_columna) not in obstaculos:
            if ((pos_fila + 1, pos_columna) in lista_pos_cajas) or ((pos_fila + 1, pos_columna) in lista_resultado):
                if ((pos_fila + 2, pos_columna) not in obstaculos) and ((pos_fila + 2, pos_columna) not in lista_pos_cajas) and ((pos_fila + 2, pos_columna) not in lista_resultado):
                    lista_acciones.append(('E', 'Abajo', (pos_fila + 1, pos_columna)))
            else:
                lista_acciones.append(('M','Abajo'))

        #   Izquierda
        if (pos_fila, pos_columna - 1) not in obstaculos:
            if ((pos_fila, pos_columna - 1) in lista_pos_cajas) or ((pos_fila, pos_columna - 1) in lista_resultado):
                if ((pos_fila, pos_columna - 2) not in obstaculos) and ((pos_fila, pos_columna - 2) not in lista_pos_cajas) and ((pos_fila, pos_columna - 2) not in lista_resultado):
                    lista_acciones.append(('E', 'Izquierda', (pos_fila, pos_columna - 1)))
            else:
                lista_acciones.append(('M','Izquierda'))

        #   Derecha
        if (pos_fila, pos_columna + 1) not in obstaculos:
            if ((pos_fila, pos_columna + 1) in lista_pos_cajas) or ((pos_fila, pos_columna + 1) in lista_resultado):
                if ((pos_fila, pos_columna + 2) not in obstaculos) and ((pos_fila, pos_columna + 2) not in lista_pos_cajas) and ((pos_fila, pos_columna + 2) not in lista_resultado):
                    lista_acciones.append(('E', 'Derecha', (pos_fila, pos_columna + 1)))
            else:
                lista_acciones.append(('M','Derecha'))

        return lista_acciones

    def result(self, state, action):
        
        pass

    def heuristic(self, state):

        pass

#------------------------------------
#Ejecutar esto para probar el actions:
#  from entrega1 import Socoban, initial, obstaculos
#  problem = Socoban(None)
#  problem.actions(initial)
#------------------------------------

#viewer = WebViewer()

#result = astar(Socoban(initial),viewer=viewer)

#print("Estado meta:")
#print(result.state)

#print("Path from initial to goal:")
#for action, state in result.path():
#    print("Haciendo", action, "llegué a:")
#    print(state)