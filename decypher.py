from PIL import Image
import numpy as np
from copy import deepcopy

def decifrar_mensaje_oculto(direc_img: str) -> str:
    """
    Recibe la dirección de una imagen con un mensaje oculto y devuelve el mensaje.
    Args:
        direc_img: dirección de la imagen con el mensaje oculto.
    Returns:
        Devuelve el mensaje oculto en la imagen.
    """

    # Lista vacía que contendrá los numeros de los caracteres ocultos
    lista_numeros_mensaje = []

    # Abrir imagen
    img_encriptada = Image.open(direc_img)

    # Convertir imagen a array de numpy.
    img_encriptada_np = np.array(img_encriptada)

    # Recorrer cada pixel de la imagen copiada.
    for i in range(0, img_encriptada_np.shape[0], 2): # Recorro las filas de a 2 pasos.
        for j in range(0, img_encriptada_np.shape[1], 2): # Por cada fila, recorro las columnas de a 2 pasos.
            
            # Tomar un entorno de 2x2
            entorno = img_encriptada_np[i:i+2, j:j+2] # i+2 va de i a i+1, el 2 no se incluye. Mismo con j.

            # Defino los 3 pixeles en los que calculo la varianza.
            pixeles_secundarios = np.array([entorno[0, 0], entorno[0, 1], entorno[1, 0]])

            # Calcular la varianza de cada canal de color por separado de los pixeles secundarios
            varianza_rojo = np.var([pixel[0] for pixel in pixeles_secundarios])
            varianza_verde = np.var([pixel[1] for pixel in pixeles_secundarios])
            varianza_azul = np.var([pixel[2] for pixel in pixeles_secundarios])

            # Obtener el canal de color con la menor varianza
            canal_menor_varianza = np.argmin([varianza_rojo, varianza_verde, varianza_azul])

            promedio_suma = 0
            # Calcular el promedio de los pixeles secundarios en el canal con menor varianza
            for pixel in pixeles_secundarios:
                promedio_suma += pixel[canal_menor_varianza]
            promedio = np.int64(promedio_suma / 3)

            # Restarle el promedio calculado al pixel inferior derecho.
            inferior_derecho = img_encriptada_np[i+1, j+1, canal_menor_varianza]
            inferior_derecho -= promedio

            # En caso de quedar un número negativo distinto a -1, se le suma 256.
            if inferior_derecho != -1 and inferior_derecho < 0:
                inferior_derecho += 256
            
            # Se agrega este resultado a la lista de números.
            lista_numeros_mensaje.append(inferior_derecho)

            # Ir a la siguiente sección hasta encontrarse que el resultado sea 0.
            if inferior_derecho == 0:
                return lista_numeros_mensaje

def escribir_mensaje(lista_numeros_mensaje):
    #Diccionario con los valores de cada caracter.
    valores = {
        "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, 
        "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, 
        "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26, " ": 27, ".": 28, 
        ",": 29, "?": 30, "!": 31, "¿": 32, "¡": 33, "(": 34, ")": 35, ":": 36, ";": 37, 
        "-": 38, "“": 39, "‘": 40, "á": 41, "é": 42, "í": 43, "ó": 44, "ú": 45, "ü": 46, "ñ": 47
    }
    # Invertir el diccionario
    valores = {v: k for k, v in valores.items()}

    # Se unen los digitos entre cada -1 para formar los números correspondientes
    mensaje_final = ""
    temp = ""
    for num in lista_numeros_mensaje:
        if num == -1:   
            mensaje_final += valores[int(temp)]
            temp = ""
        else:
            temp += str(num - 1)


    return mensaje_final
        
#print(decifrar_mensaje_oculto("encrypted_baboon.png"))
direc_imagen_encriptada = input("Ingrese la dirección de la imagen con el mensaje oculto: ")
print(escribir_mensaje(decifrar_mensaje_oculto(direc_imagen_encriptada)))