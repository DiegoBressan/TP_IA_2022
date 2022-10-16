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
# -Primera tupla donde guardamos la posición del jugador
# -Segunda tupla (Lista de las posiciones actuales de las cajas en el mapa)
# -Tercera tupla lista inicialmente vacia (iremos almacenando y sacando las cajas de la lista a medida que se encuentren en su posición)
# -Cuarta tupla (Lista de posiciones actuales de lugares correctos)
# -Quinta tupla lista inicialmente vacia (iremos almacenando y sacando los lugares correctos para saber cuales quedan)
initial = (

    (1, 4),
    ((2, 3), (3, 4), (4, 4), (6, 1), (6, 3), (6, 4), (6, 5)),
    (),
    ((2, 1), (3, 5), (4, 1), (5, 4), (6, 3), (7, 4), (6, 6)),
    (),
    50

)

obstaculos = (
(0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 0), (1, 1), (1, 2), (1, 6), 
(2, 0), (2, 6), (3, 0), (3, 1), (3, 2), (3, 6), (4, 0), (4, 2), (4, 3), 
(4, 6), (5, 0), (5, 2), (5, 6), (5, 7), (6, 0), (6, 7), (7, 0), (7, 7), 
(8, 0), (8, 1), (8, 2), (8, 3), (8, 4), (8, 5), (8, 6), (8, 7),
)


from simpleai.search.viewers import WebViewer, BaseViewer

class Socoban(SearchProblem):

    def cost(self, state, action, state2):
        
        return 1

    def is_goal(self, state):

        if (state[1] == () and state[3] == ()):
            return True 

    def actions(self, state):

        pos_jugador, lista_pos_cajas, lista_resultado, lista_pos_correctos, lista_resultado2, _ = state
        pos_fila = pos_jugador[0]
        pos_columna = pos_jugador[1]

        #La lista de acciones esta compuesta por 3 tuplas en el caso que se deba mover una caja
        #1- El movimiento del personaje
        #2- El movimiento de la caja
        #3- 'Empujar' si hay que empujar una caja o 'Mover' si solo hay que mover el personaje
        lista_acciones = []
        
        movimientos = []
        movimientos.append((pos_fila - 1, pos_columna)) #arriba
        movimientos.append((pos_fila + 1, pos_columna)) #abajo
        movimientos.append((pos_fila, pos_columna - 1)) #izquierda
        movimientos.append((pos_fila, pos_columna + 1)) #derecha

        for indicemov, movimiento in enumerate(movimientos):
            #Pregunto si el movimiento es posible y no hay pared..
            if movimiento not in obstaculos:
                #Pregunto si me encuentro pegado a una caja
                if movimiento in lista_pos_cajas:
                    if indicemov == 0: #Si esta parado debajo de una caja
                        auxfila, auxcolumna = movimiento
                        band = 0
                        #Recorro la lista de obstaculos y pregunto si del otro lado de la caja hay un obstaculo
                        for obstaculo in obstaculos:
                            if (auxfila - 1, auxcolumna) == obstaculo:
                                band = 1
                                break
                        #Si no hay ningun obstaculo, puedo mover la caja
                        if band == 0:
                            lista_acciones.append((movimiento, (auxfila - 1, auxcolumna), 'Empujar'))
                    if indicemov == 1: #Si esta parado arriba de una caja
                        auxfila, auxcolumna = movimiento
                        band = 0
                        for obstaculo in obstaculos:
                            if (auxfila + 1, auxcolumna) == obstaculo:
                                band = 1
                                break
                        if band == 0:
                            lista_acciones.append((movimiento, (auxfila + 1, auxcolumna), 'Empujar'))
                    if indicemov == 2: #Si esta parado a la Derecha de una caja
                        auxfila, auxcolumna = movimiento
                        band = 0
                        for obstaculo in obstaculos:
                            if (auxfila, auxcolumna - 1) == obstaculo:
                                band = 1
                                break
                        if band == 0:
                            lista_acciones.append((movimiento, (auxfila, auxcolumna - 1), 'Empujar'))
                    if indicemov == 3: #Si esta parado a la Izquierda de una caja
                        auxfila, auxcolumna = movimiento
                        band = 0
                        for obstaculo in obstaculos:
                            if (auxfila, auxcolumna + 1) == obstaculo:
                                band = 1
                                break
                        if band == 0:
                            lista_acciones.append((movimiento, (auxfila, auxcolumna + 1), 'Empujar'))
                else:
                    lista_acciones.append((movimiento, 'Mover'))
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