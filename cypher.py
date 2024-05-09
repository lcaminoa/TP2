from funciones import encriptador_mensaje, esconder_mensaje_imagen

print("≡≡Encriptador≡≡")
img_base = input("Ingrese nombre de la imagen a utilizar como base: ")
mensaje = input("Ingrese el mensaje a esconder: ")
salida = input("Ingrese nombre del archivo de salida: ")

mensaje_encriptado = encriptador_mensaje(mensaje)
# Guardar la imagen con el mensaje escondido.
imagen_encriptada = esconder_mensaje_imagen(img_base, mensaje_encriptado)
imagen_encriptada.save(salida)