
# TC1028. Pensamiento Computacional para Ingeniería
#
# Lucca Traslosheros Abascal
# 25 de septiembre de 2025
# Prototipo del Proyecto


def mostrar_tablero(tablero, movimientos):
    # Muestra el tablero y el contador de movimientos
    print("\n====================")

    for fila in tablero:
        print(" ".join(fila))
        
    print(f"Movimientos: {movimientos}")
    print("====================")

def calcular_nueva_posicion(posicion, movimiento):
    # Calcula la nueva coordenada
    # Guarda posicion en una lista de 2 indices
    # [fila, columna]
    # Tambien puede ser un tuple 

    nueva_pos = list(posicion)
    if movimiento == 'w':
        nueva_pos[0] -= 1
    elif movimiento == 's':
        nueva_pos[0] += 1
    elif movimiento == 'a':
        nueva_pos[1] -= 1
    elif movimiento == 'd':
        nueva_pos[1] += 1
    return nueva_pos

def es_movimiento_valido(tablero, posicion):
    # Verifica si el movimiento esta dentro de los limites 
    # y que no es una pared

    fila, col = posicion
    # si no esta out of bounds
    if 0 <= fila < len(tablero) and 0 <= col < len(tablero[0]):
        if tablero[fila][col] != '#':
            # y si no es pared
            return True
    # si no falso
    return False

def jugar():
    # Logica del juego general

    # Laberinto y posicion de todo esta hard coded
    # El laberinto se representa como una matriz que es una lista de listas.
    laberinto = [
        ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', 'P', '.', '#', '.', '.', '.', '.', '#'],
        ['#', '.', '.', '#', '.', '#', '#', '.', '#'],
        ['#', '.', '#', '#', '.', '.', '#', '.', '#'],
        ['#', '.', '.', '.', '.', '#', '#', '.', 'E'],
        ['#', '#', '#', '#', '#', '#', '#', '#', '#']
    ]

    # Coordenadas iniciales [fila, columna]
    # variables iniciales
    posicion_jugador = [1, 1]
    posicion_salida = [4, 8]
    movimientos = 0
    juego_activo = True

    print("--- Inicio del Juego del Laberinto ---")
    print("Usa 'w','a','s','d' para moverte. Escribe 'salir' para terminar.")

    while juego_activo:
        mostrar_tablero(laberinto, movimientos)

        # Condición de victoria.
        # Falta hacer

        # Para no ser infinito acaba despues de 20 movimientos
        if movimientos > 20:
            juego_activo = False


        # Entrada: Pide el movimiento al usuario.
        movimiento = input("Tu movimiento: ")

        # Falta checar si es input valido

        
        # asigna la nueva posicion de acuerdo al movimiento del jugador
        nueva_posicion = calcular_nueva_posicion(posicion_jugador, movimiento)
        
        # si el movimiento es valido entonces
        if es_movimiento_valido(laberinto, nueva_posicion):
            # borra la posición anterior del jugador.
            laberinto[posicion_jugador[0]][posicion_jugador[1]] = '.'

            # Actualiza la nueva posición.
            posicion_jugador = nueva_posicion
            laberinto[posicion_jugador[0]][posicion_jugador[1]] = 'P'
            movimientos += 1
        # Si no entonces no se mueve nada
        else:
            print("Movimiento inválido. Intenta de nuevo.")


    # Cuando se acabe se termina el juego
    print("\n--- Juego Terminado ---")

# Punto de entrada para iniciar el juego.
def main():
    jugar()
    
main()