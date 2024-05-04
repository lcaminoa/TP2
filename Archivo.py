import numpy as np
from PIL import Image
from copy import deepcopy

# Abrir imagen
img = Image.open("baboon.jpg")

# Convertir imagen a array de numpy
img_np = np.array(img)

# Añadir padding de 2 pixeles con el color del pixel más cercano
img_np_padding = np.pad(img_np, ((2, 2), (2, 2), (0, 0)), mode="edge")

# Crear una copia profunda de la imagen array con el padding
img_copy = deepcopy(img_np_padding)

# Recorrer cada pixel de la imagen copiada
for i in range(2, img_copy.shape[0]-2):
    for j in range(2, img_copy.shape[1]-2):
        
        # Tomar un entorno de 5x5
        entorno = img_copy[i-2:i+3, j-2:j+3]
        
        # Dividir este entorno en cuatro cuadrantes
        cuadrantes = [entorno[:2, :2], entorno[:2, 2:], entorno[2:, :2], entorno[2:, 2:]]

        # Puede que haya un error y no incluya la cruz. Sol: Que el slicing termine en 3.
        
        # Calcular la varianza de los canales rojo, verde y azul y sumar estas varianzas
        varianzas = [np.var(cuadrante, axis=(0, 1)) for cuadrante in cuadrantes] # Se agrega a la lista las varianzas de cada cuadrante
        """
        axis=(0, 1) estaría calculando la varianza de cada canal de color en cada cuadrante.
        """
        varianzas_totales = [np.sum(varianza) for varianza in varianzas]
        
        # Seleccionar el cuadrante con la suma de varianzas más baja
        cuadrante_varianza_minima = cuadrantes[np.argmin(varianzas_totales)]
        
        # Calcular el promedio de cada color para los pixeles del cuadrante seleccionado
        color_promedio = np.mean(cuadrante_varianza_minima, axis=(0, 1))
        
        # Asignar este promedio al pixel actual en la imagen copiada
        img_copy[i, j] = color_promedio

# Devolver la imagen copiada modificada

