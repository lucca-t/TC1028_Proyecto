# Evidencia 2
# Proyecto Integrador TC1028 Pensamiento Computacional para Ingeniería
# Grupo 417
# Autor: Lucca Traslosheros Abascal
#
# Este proyecto usa un laberinto precargado o un archivo de texto
# para jugar el laberinto en una interfaz gráfica.
# Usa una matriz para los posiciones y las dibuja con tkinter
# Todo esta en metodos para validar los movimientos y actualizar el juego


import tkinter as tk
from tkinter import font


CELL_SIZE = 60  # Tamaño de cada celda en píxeles


def cargar_laberinto(archivo):
    """
    Entrada: Archivo de texto.
    Proceso: Procesar el texto para convertir en matriz.
    Salida: Lista de listas de laberinto o vacio si esta incorrecto el archivo.
    """
    lineas = []
    try:
        with open(archivo, "r") as f:
            lineas = [list(line.strip("\n")) for line in f.readlines()]
        return lineas
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{archivo}'")
        return []


def configurar_laberinto(usar_archivo=False, nombre_archivo=""):
    """
    Entrada: Archivo o nada
    Proceso: Configurar los valores para iniciar el laberinto
    Salida: Valores de laberinto
    """
    if usar_archivo:
        laberinto = cargar_laberinto(nombre_archivo)
        if not laberinto:
            print("Usando el laberinto predefinido por error de archivo.")
    else:
        laberinto = []

    # laberinto por defecto
    if not laberinto:
        laberinto = [
            ['#', '#', '#', '#', '#', '#', '#', '#', '#'],
            ['#', 'P', '.', '#', '.', '.', '.', '.', '#'],
            ['#', '.', '.', '#', '.', '#', '#', '.', '#'],
            ['#', '.', '#', '#', '.', '.', '#', '.', '#'],
            ['#', '.', '.', '.', '.', '#', '#', '.', 'E'],
            ['#', '#', '#', '#', '#', '#', '#', '#', '#']
        ]

    posicion_jugador = []
    posicion_salida = []

    # Configurar posicion de inicio salida
    for i, fila in enumerate(laberinto):
        for j, celda in enumerate(fila):
            if celda == 'P':
                posicion_jugador = [i, j]
            elif celda in ('E', 'X'):
                posicion_salida = [i, j]

    return laberinto, posicion_jugador, posicion_salida


def dibujar_laberinto(canvas, laberinto):
    """
    Entrada: Canvas de Tkinter y estatus actual de laberinto
    Proceso: Dibujar todas las posiciones en texto para usar visualizar en Tkinter
             Cambiar color dependiendo de tipo de bloque con outline
    Salida: Canvas de Tkinter actualizado
    """
    canvas.delete("all")

    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            x1 = col * CELL_SIZE
            y1 = fila * CELL_SIZE
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE

            celda = laberinto[fila][col]

            if celda == '#':
                color = "black"
            elif celda == 'P':
                color = "blue"
            elif celda in ('E', 'X'):
                color = "green"
            else:
                color = "white"

            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")


def calcular_nueva_posicion(pos, mov):
    """
    Entrada: posicion actual del jugador y la tecla ingresada
    Proceso: Cambiar la fila o columna dependiendo del movimiento
    Salida: Devuelve la nueva posición según la tecla (w/a/s/d).
    """

    fila, col = pos

    if mov == 'w':
        fila -= 1
    elif mov == 's':
        fila += 1
    elif mov == 'a':
        col -= 1
    elif mov == 'd':
        col += 1

    return [fila, col]



def es_valido(laberinto, pos):
    """
    Entrada: Matriz de laberinto, posicion de jugador
    Proceso: Verificar si la posicion nueva es valida
    Salida: True or False
    """
    fila, col = pos
    if 0 <= fila < len(laberinto) and 0 <= col < len(laberinto[0]):
        return laberinto[fila][col] != '#'
    else:
        return False


def mover(tecla, laberinto, canvas, ventana, posicion_jugador,
          posicion_salida, movimientos):
    """
    Entrada: Event de teclado, matriz del laberinto, canvas y ventana de 
    tkinter, posicion del jugador, posicion del final, cantidad de movimientos
    Proceso: Actualizar nuevo movimiento visualmente
    Salida: Posicion y movimientos actualizados 
    Gestiona el movimiento del jugador y verifica si ha llegado a la meta.
    Devuelve la nueva posición y el número actualizado de movimientos.
    """

    # Solo considerar (w/a/s/d) para movimientos
    
    if tecla not in ['w', 'a', 's', 'd']:
        return posicion_jugador, movimientos

    # Actualizar posicion nueva
    nueva = calcular_nueva_posicion(posicion_jugador, tecla)

    # Actualizar posicion
    if es_valido(laberinto, nueva):
        # Cambiar posicion previa a vacio
        laberinto[posicion_jugador[0]][posicion_jugador[1]] = '.'
        posicion_jugador = nueva
        movimientos += 1

        # Cambiar si es ganador 
        if posicion_jugador == posicion_salida:
            laberinto[posicion_jugador[0]][posicion_jugador[1]] = 'P'
            dibujar_laberinto(canvas, laberinto)

            # Poner el texto en medio de la pantalla
            canvas.create_text(
                len(laberinto[0]) * CELL_SIZE // 2,
                len(laberinto) * CELL_SIZE // 2,
                text=f"¡Ganaste en {movimientos} movimientos!",
                fill="red",
                font=("Comic Sans MS", 22, "bold")
            )
            # No permitir nuevos movimientos y retornar
            ventana.unbind("w")
            ventana.unbind("a")
            ventana.unbind("s")
            ventana.unbind("d")
            return posicion_jugador, movimientos

        laberinto[posicion_jugador[0]][posicion_jugador[1]] = 'P'
        dibujar_laberinto(canvas, laberinto)

    return posicion_jugador, movimientos


def main():
    """Función principal del juego."""
    usar_archivo = input("¿Quieres usar tu propio laberinto? (s/n): ").lower() == 's'
    # Usar archivo es bool, y llamar funcion apropiada
    if usar_archivo:
        nombre_archivo = input("Nombre del archivo (eg. laberinto.txt): ")
        laberinto, posicion_jugador, posicion_salida = configurar_laberinto(
            True, nombre_archivo
        )
    else:
        laberinto, posicion_jugador, posicion_salida = configurar_laberinto()

    # Iniciar variables y ventana
    movimientos = 0

    ventana = tk.Tk()
    ventana.title("Juego del Laberinto")

    # Configurar ventana dinamicamente
    canvas = tk.Canvas(
        ventana,
        width=len(laberinto[0]) * CELL_SIZE,
        height=len(laberinto) * CELL_SIZE,
        bg="white"
    )
    canvas.pack()

    dibujar_laberinto(canvas, laberinto)

    # Mini metodo que llama mover si se presiona tecla de movimiento
    # nonlocal para que use los valores edl main
    def mover_direccion(tecla):
        nonlocal posicion_jugador, movimientos
        posicion_jugador, movimientos = mover(
            tecla, laberinto, canvas, ventana,
            posicion_jugador, posicion_salida, movimientos
        )
    
    ventana.bind("w", lambda e: mover_direccion('w'))
    ventana.bind("a", lambda e: mover_direccion('a'))
    ventana.bind("s", lambda e: mover_direccion('s'))
    ventana.bind("d", lambda e: mover_direccion('d'))

    
    
    ventana.mainloop()


if __name__ == "__main__":
    main()
