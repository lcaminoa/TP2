from funciones import escribir_mensaje, decifrar_mensaje_oculto

print("≡≡Desencriptador≡≡")
direc_imagen_encriptada = input("Ingrese nombre del archivo encriptado: ")
print("")
mensaje = escribir_mensaje(decifrar_mensaje_oculto(direc_imagen_encriptada))
print(f"El mensaje oculto es: {mensaje}")