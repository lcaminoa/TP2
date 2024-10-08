import numpy as np
from PIL import Image
from copy import deepcopy

def filtro_kuwahara(direc_img: str) -> np.ndarray:
    """
    Recibe la dirección de una imagen y le aplica el filtro Kuwahara, luego se guarda en el dispositivo.
    Args:
        direc_img: dirección de la imagen a aplicar el filtro Kuwahara.
    Returns:
        Devuelve la imagen en formato de array de numpy.
    """
    img = Image.open(direc_img)

    img_np = np.array(img)

    # Añadir padding de 2 pixeles con el color del pixel más cercano.
    img_np_padding = np.pad(img_np, ((2, 2), (2, 2), (0, 0)), mode="edge")

    img_copy = deepcopy(img_np_padding)

    for i in range(2, img_copy.shape[0]-2):
        for j in range(2, img_copy.shape[1]-2):
            
            # Entorno de 5x5
            entorno = img_copy[i-2:i+3, j-2:j+3]
            
            cuadrantes = [entorno[:3, :3], entorno[:3, 2:], entorno[2:, :3], entorno[2:, 2:]]

            # Calcular la varianza de los canales rojo, verde y azul y sumar estas varianzas.
            varianzas = [np.var(cuadrante, axis=(0, 1)) for cuadrante in cuadrantes]
            
            varianzas_totales = [np.sum(varianza) for varianza in varianzas]
            
            cuadrante_varianza_minima = cuadrantes[np.argmin(varianzas_totales)]
            
            color_promedio = np.mean(cuadrante_varianza_minima, axis=(0, 1))
            
            # Asignar este promedio al pixel actual
            img_np_padding[i, j] = color_promedio

    # Quitar padding
    img_np_final = img_np_padding[2:-2, 2:-2, :]       

    return img_np_final

def encriptador_mensaje(mensaje: str) -> list:
    """
    Recibe un mensaje a encriptar y lo convierte en una lista de números.
    Args:
        mensaje: Mensaje a encriptar.
    Returns:
        Devuelve la lista con los valores del mensaje encriptado.
    """
    valores = {
        "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, 
        "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, 
        "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26, " ": 27, ".": 28, 
        ",": 29, "?": 30, "!": 31, "¿": 32, "¡": 33, "(": 34, ")": 35, ":": 36, ";": 37, 
        "-": 38, "“": 39, "‘": 40, "á": 41, "é": 42, "í": 43, "ó": 44, "ú": 45, "ü": 46, "ñ": 47
    }
    mensaje = mensaje.lower()
    
    mensaje_traducido = [valores[caracter] for caracter in mensaje]

    mensaje_codificado = []

    for numero in mensaje_traducido:
        for caracter in str(numero):
            mensaje_codificado.append(int(caracter) + 1)
        mensaje_codificado.append(-1)


    mensaje_codificado.append(0)
    return mensaje_codificado

def esconder_mensaje_imagen(direc_imagen: str, mensaje_encriptado: list) -> Image:
    """
    Recibe un mensaje encriptado y lo esconde en una imagen.
    Args:
        direc_imagen: Dirección de la imagen en la que se esconderá el mensaje.
        mensaje_encriptado: Mensaje encriptado.
    Returns:
        Devuelve la imagen con el mensaje escondido.
    """
    # Imagen array con el filtro ya aplicado.
    imagenArray = filtro_kuwahara(direc_imagen)

    index_del_mensaje = 0
    for i in range(0, imagenArray.shape[0], 2):
            for j in range(0, imagenArray.shape[1], 2):
                
                # Entorno de 2x2
                entorno = imagenArray[i:i+2, j:j+2]
            
                pixel_primario = entorno[1, 1]
                
                pixeles_secundarios = [entorno[0, 0], entorno[0, 1], entorno[1, 0]]
        
                varianza_rojo = np.var([pixel[0] for pixel in pixeles_secundarios])
                varianza_verde = np.var([pixel[1] for pixel in pixeles_secundarios])
                varianza_azul = np.var([pixel[2] for pixel in pixeles_secundarios])

                canal_menor_varianza = np.argmin([varianza_rojo, varianza_verde, varianza_azul])

                if index_del_mensaje <= len(mensaje_encriptado)-1:
                
                    promedio_suma = 0
                    # Calcular el promedio de los pixeles secundarios en el canal con menor varianza
                    for pixel in pixeles_secundarios:
                        promedio_suma += pixel[canal_menor_varianza]
                    promedio = promedio_suma / 3
                
                    nuevo_pixel = (promedio + mensaje_encriptado[index_del_mensaje]) % 256
                
                    # Asignar este promedio al pixel primario en el canal calculado
                    pixel_primario[canal_menor_varianza] = nuevo_pixel

                    index_del_mensaje += 1
    Imagen_final = Image.fromarray(imagenArray)
    return Imagen_final

def decifrar_mensaje_oculto(direc_img: str) -> str:
    """
    Recibe la dirección de una imagen con un mensaje oculto y devuelve el mensaje.
    Args:
        direc_img: dirección de la imagen con el mensaje oculto.
    Returns:
        Devuelve el mensaje oculto en la imagen.
    """
    lista_numeros_mensaje = []

    img_encriptada = Image.open(direc_img)

    img_encriptada_np = np.array(img_encriptada)

    for i in range(0, img_encriptada_np.shape[0], 2):
        for j in range(0, img_encriptada_np.shape[1], 2):
            
            # Entorno de 2x2
            entorno = img_encriptada_np[i:i+2, j:j+2]

            pixeles_secundarios = np.array([entorno[0, 0], entorno[0, 1], entorno[1, 0]])

            varianza_rojo = np.var([pixel[0] for pixel in pixeles_secundarios])
            varianza_verde = np.var([pixel[1] for pixel in pixeles_secundarios])
            varianza_azul = np.var([pixel[2] for pixel in pixeles_secundarios])

            canal_menor_varianza = np.argmin([varianza_rojo, varianza_verde, varianza_azul])

            promedio_suma = 0
            # Calcular el promedio de los pixeles secundarios en el canal con menor varianza
            for pixel in pixeles_secundarios:
                promedio_suma += pixel[canal_menor_varianza]
            promedio = np.int64(promedio_suma / 3)

            # Restarle el promedio al pixel inferior derecho.
            inferior_derecho = img_encriptada_np[i+1, j+1, canal_menor_varianza]
            inferior_derecho -= promedio

            if inferior_derecho != -1 and inferior_derecho < 0:
                inferior_derecho += 256
            
            lista_numeros_mensaje.append(inferior_derecho)

            if inferior_derecho == 0:
                return lista_numeros_mensaje

def escribir_mensaje(lista_numeros_mensaje):
    valores = {
        "a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, "h": 8, "i": 9, "j": 10, 
        "k": 11, "l": 12, "m": 13, "n": 14, "o": 15, "p": 16, "q": 17, "r": 18, "s": 19, 
        "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26, " ": 27, ".": 28, 
        ",": 29, "?": 30, "!": 31, "¿": 32, "¡": 33, "(": 34, ")": 35, ":": 36, ";": 37, 
        "-": 38, "“": 39, "‘": 40, "á": 41, "é": 42, "í": 43, "ó": 44, "ú": 45, "ü": 46, "ñ": 47
    }

    # Invertir el diccionario
    valores = {v: k for k, v in valores.items()}

    mensaje_final = ""
    temp = ""
    for num in lista_numeros_mensaje:
        if num == -1:   
            mensaje_final += valores[int(temp)]
            temp = ""
        else:
            temp += str(num - 1)


    return mensaje_final