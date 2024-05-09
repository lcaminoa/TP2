import numpy as np
from PIL import Image
from copy import deepcopy

def filtro_kuwahara(direc_img):
    """
    Recibe la dirección de una imagen y le aplica el filtro Kuwahara, luego se guarda en el dispositivo.
    Args:
        direc_img: dirección de la imagen a aplicar el filtro Kuwahara.
    """
    # Abrir imagen
    img = Image.open(direc_img)

    # Convertir imagen a array de numpy.
    img_np = np.array(img)

    # Añadir padding de 2 pixeles con el color del pixel más cercano.
    img_np_padding = np.pad(img_np, ((2, 2), (2, 2), (0, 0)), mode="edge")

    # Crear una copia profunda de la imagen array con el padding.
    img_copy = deepcopy(img_np_padding)

    # Recorrer cada pixel de la imagen copiada.
    for i in range(2, img_copy.shape[0]-2):
        for j in range(2, img_copy.shape[1]-2):
            
            # Tomar un entorno de 5x5
            entorno = img_copy[i-2:i+3, j-2:j+3]
            
            # Dividir este entorno en cuatro cuadrantes.
            cuadrantes = [entorno[:3, :3], entorno[:3, 2:], entorno[2:, :3], entorno[2:, 2:]]

            # El slicing termina en :3 porque el 3 no se incluye, queda de 0 a 2.

            # Calcular la varianza de los canales rojo, verde y azul y sumar estas varianzas.
            varianzas = [np.var(cuadrante, axis=(0, 1)) for cuadrante in cuadrantes] # Se agrega a la lista las varianzas de cada cuadrante.
            """
            axis=(0, 1) estaría calculando la varianza de cada canal de color en cada cuadrante.
            """
            varianzas_totales = [np.sum(varianza) for varianza in varianzas]
            
            # Seleccionar el cuadrante con la suma de varianzas más baja
            cuadrante_varianza_minima = cuadrantes[np.argmin(varianzas_totales)]
            
            # Calcular el promedio de cada color para los pixeles del cuadrante seleccionado
            color_promedio = np.mean(cuadrante_varianza_minima, axis=(0, 1))
            
            # Asignar este promedio al pixel actual en la imagen ORIGINAL con padding
            img_np_padding[i, j] = color_promedio

    # Quitar padding de la imagen con padding
    img_np_final = img_np_padding[2:-2, 2:-2, :]       

    # Devolver la imagen final
    return img_np_final

def encriptador_mensaje(mensaje):
    #Diccionario con los valores de cada caracter.
    valores = {
        "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, 
        "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, 
        "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26, " ": 27, ".": 28, 
        ",": 29, "?": 30, "!": 31, "¿": 32, "¡": 33, "(": 34, ")": 35, ":": 36, ";": 37, 
        "-": 38, "“": 39, "‘": 40, "á": 41, "é": 42, "í": 43, "ó": 44, "ú": 45, "ü": 46, "ñ": 47
    }

    mensaje_traducido = [valores[caracter] for caracter in mensaje] # Se convierte el mensaje en una lista con cada valor.

    mensaje_codificado = []

    for numero in mensaje_traducido:
        for caracter in str(numero):
            mensaje_codificado.append(int(caracter) + 1)
        mensaje_codificado.append(-1)

    # Se agrega un 0 al final del mensaje.
    mensaje_codificado.append(0)


mensaje = input("Ingrese un mensaje: ").lower() # Se convierte el mensaje a minúsculas.
encriptador_mensaje(mensaje) # Encripto el mensaje llamado la funcion con el mensaje ingresado.

# Llamo a la funcion del filtro y guardo la imagen ya hecha array en una variable.
imagenArray = filtro_kuwahara("baboon.jpg")

# Necesito que me ...?
for i in range(0, imagenArray.shape[0], 2): # Recorro las filas de a 2 pasos.
        for j in range(0, imagenArray.shape[1], 2): # Por cada fila, recorro las columnas de a 2 pasos.
            
            # Tomar un entorno de 2x2
            entorno = imagenArray[i:i+2, j:j+2] # i+2 va de i a i+1, el 2 no se incluye. Mismo con j.
        
            pixel_primario = entorno[1, 1]
            
            # Defino los 3 pixeles en los que calculo la varianza (no terminado)
            pixeles_secundarios = [entorno[0][0], entorno[0][1], entorno[1][0]]
            print(pixeles_secundarios)
    
            # Calcular la varianza de cada canal de color por separado de los secundarios
            varianza_rojo = np.var([pixel[0] for pixel in pixeles_secundarios])
            varianza_verde = np.var([pixel[1] for pixel in pixeles_secundarios])
            varianza_azul = np.var([pixel[2] for pixel in pixeles_secundarios])

            # Obtener el canal de color con la menor varianza
            canal_menor_varianza = np.argmin([varianza_rojo, varianza_verde, varianza_azul])
            #print(canal_menor_varianza)

            promedio_suma = 0
            # Calcular el promedio de los pixeles secundarios en el canal con menor varianza
            for pixel in pixeles_secundarios:
                promedio_suma += pixel[canal_menor_varianza]
            promedio = promedio_suma / 3

            # Asignar este promedio al pixel primario en el canal calculado
            pixel_primario[canal_menor_varianza] = promedio