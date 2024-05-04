import numpy as np
from PIL import Image

# Abrir imagen
img = Image.open("baboon.jpg")

# Convertir imagen a array de numpy
img_np = np.array(img)

# Añadir padding de 2 pixeles con el color del pixel más cercano
img_np_padding = np.pad(img_np, ((2, 2), (2, 2), (0, 0)), mode="edge")

#Convertir la matriz NumPy a una imagen PIL y guardarla
img_padding = Image.fromarray(img_np_padding)
img_padding.save('imagen_padding.jpg')

print("Hola")
print("Chau")