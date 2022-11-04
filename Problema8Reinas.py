#Título Programa: PRACTICA 2---Problema de las 8 Reinas.
#Fecha: 21-octubre-2022
#Autor: Renteria Arriaga Josue

# Funciones
# -------------------------------------------------------------------------------------------------------------------
# Exportación de las librerías a utilizar. 
import random # Esta librería nos ayuda a generar números aleatorios.
import numpy as np # Esta librería nos ayudara a utilizar arrays (para sacar el promedio).
from tkinter import * # Librería para crear el tablero gráfico.
import copy # Para hacer una copia del arreglo de forma profunda.

# Función Recursiva que saca la Heurística de los pares Hn = (n-1) + Hn-1
def heuristica_pares(numero):
    if numero == 0:
        return 0 # Para el Caso Base.
    else:
        return ((numero - 1) + heuristica_pares(numero -1)) #Caso de Estudio.

# Función que saca la Heurística de nuestro tablero de forma horizontal.
def conteo_horizontal(array):
    heuristica = 0
    for i in range(8):
        contador = 0
        for j in range(8):
            if array[i,j] == 1:
                contador += 1

        # Mandamos a llamar al Contador.
        heuristica += heuristica_pares(contador)
    return heuristica

# Función que saca la Heurística de nuestro tablero de forma Diagonal.
def conteo_diagonal(array):
    heuristica = 0
    lista1 = []
    lista2 = []
    for i in range(8):
        for j in range(8):
            contador1 = 0
            contador2 = 0

            # Hace la Búsqueda de Derecha a Abajo (Eje. (2,3)-(3,4)). 
            if array[i,j] == 1 and (lista1.count((i,j)) == 0):
                x = i
                y = j
                while (x < 8 and y < 8):
                    if array[x,y] == 1:
                        lista1.append((x,y)) # Agregamos la dupla a una lista (Para no repetir elementos).
                        contador1 += 1
                    x = x + 1
                    y = y + 1
            
            # Hace la Búsqueda de Abajo a Izquierda (Eje. (2,3)-(1,4)). 
            if array[i,j] == 1 and (lista2.count((i,j)) == 0):
                x = i
                y = j
                while (x < 8  and y > -1):
                    if array[x,y] == 1:
                        lista2.append((x,y)) # Agregamos la dupla a una lista (Para no repetir elementos).
                        contador2 += 1
                    x = x + 1
                    y = y - 1

            # Mandamos a llamar a los contadores y le agregamos su heurística.
            heuristica += heuristica_pares(contador1)
            heuristica += heuristica_pares(contador2)
    return heuristica

# Funcion que saca la Heuristica Total del Problema.
def heuristica_metodo(array):
    heuristica = conteo_diagonal(array) + conteo_horizontal(array)
    return heuristica

# Funcion que llena la columna deseada con ceros.
def llennar_columna(array, x):
    for i in range(8):
            array[i, x] = 0
    return array 
# -------------------------------------------------------------------------------------------------------------------

# Creación del Arreglo Bidimensional de 8x8 y Rellenar el Arreglo Bidimensional de 8x8 con 1.
tablero_inicial = np.zeros((8, 8), dtype=np.int64) # Arreglo Bidimensional 8x8.
tablero_nuevo = np.zeros((8, 8), dtype=np.int64)
tablero_final = np.zeros((8, 8), dtype=np.int64)
tablero2 = np.zeros((8, 8), dtype=np.int64)

for i in range(8):
    movimiento = random.randint(0,7)
    tablero_inicial[movimiento, i] = 1
print(tablero_inicial) # Observar el Arreglo Final (utilizar para sacar la heurística)

# Sacar la heurística Horizontal y Diagonal.
heuristica_horizontal = conteo_horizontal(tablero_inicial) # Horizontal.
print("\n\n")
print(f"La Heurística Horizontal es de: {heuristica_horizontal}")
heuristica_diagonal = int(conteo_diagonal(tablero_inicial)) # Diagonal
print(f"La Heurística Diagonal es de: {heuristica_diagonal}")

# Sacar la heurística Total.
heuristica_total = heuristica_metodo(tablero_inicial)
print(f"La Heurística Total es de: {heuristica_total}\n")

# Arreglo Final, que entrara a la funcion.
tablero2 = tablero_inicial
total = 0

# Proceso para cambiar el arreglo con la mejor heuristica
for i in range(8):
    tablero_final =  copy.deepcopy(tablero2)
    for j in range(8):

        # Cambiamos el 1 del arreglo a otra posicion.
        tablero_nuevo = llennar_columna(tablero_final, i)
        tablero_nuevo[j,i] = 1
        nueva_heuristica = int(heuristica_metodo(tablero_nuevo))

        #Muestra de los casos de Estudio.
        print(tablero_nuevo)
        print(f"Estamos en la columna:{i} y fila {j}")
        print(f"Con la mejor Heuristica de:{nueva_heuristica}\n")

        # Tomar la menor Heuristica.
        if (nueva_heuristica < heuristica_total):
            tablero2 = copy.deepcopy(tablero_nuevo)
            heuristica_total = nueva_heuristica
        #elif (nueva_heuristica == heuristica_total):
        #    tablero2 =  copy.deepcopy(tablero_final)
        
# La mejor Opcion
print("\n\n\nEl que que quedo al final es:")
print(tablero2)
print(f"Con heuristica de:{heuristica_total}")

# Funciones
# -------------------------------------------------------------------------------------------------------------------
# Graficar el tablero (Creación de la Ventana para el Tablero Inicial). 
root = Tk()
root.title("Tablero Inicial")
Grid.rowconfigure(root, 0, weight=10)
Grid.columnconfigure(root, 0, weight=10)
root.geometry("500x500")

# Creamos y configuramos un Frame.
frame = Frame(root)
frame.grid(row = 0, column = 0, sticky = N+S+E+W)
indice = 0

#Creamos un 8x8 (filas y columnas).
for filas in range(8):
    Grid.rowconfigure(frame, filas, weight = 10)
    for columnas in range(8):
        Grid.columnconfigure(frame, columnas, weight = 10)

        # Coloreamos los Botones que tengan un 1 en el arreglo.
        if tablero_inicial[filas, columnas] == 1:
            btn = Button(frame, bg = "blue") # Creación de los botones en el Frame (Los que tengan a la reina).
        else:
            btn = Button(frame) # Creación de los botones en el Frame (los que quedan). 
        btn.grid(row = filas, column = columnas, sticky = N+S+E+W)  

# Graficar el tablero (Creación de la Ventana para el Tablero Final). 
root2 = Tk()
root2.title("Tablero Final")
Grid.rowconfigure(root2, 0, weight=10)
Grid.columnconfigure(root2, 0, weight=10)
root2.geometry("500x500")

# Creamos y configuramos un Frame.
frame = Frame(root2)
frame.grid(row = 0, column = 0, sticky = N+S+E+W)
indice = 0

#Creamos un 8x8 (filas y columnas).
for filas in range(8):
    Grid.rowconfigure(frame, filas, weight = 10)
    for columnas in range(8):
        Grid.columnconfigure(frame, columnas, weight = 10)

        # Coloreamos los Botones que tengan un 1 en el arreglo.
        if tablero2[filas, columnas] == 1:
            btn = Button(frame, bg = "blue") # Creación de los botones en el Frame (Los que tengan a la reina).
        else:
            btn = Button(frame) # Creación de los botones en el Frame (los que quedan). 
        btn.grid(row = filas, column = columnas, sticky = N+S+E+W)  

# Loop de la Ventana.
root.mainloop()
# -------------------------------------------------------------------------------------------------------------------