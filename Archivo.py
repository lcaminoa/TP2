from PIL import Image
import numpy as np

# Abrir imagen
img = np.array(Image.open('baboon.jpg'))

# Dimensiones de la imagen
altura, ancho, canales = img.shape

# Añadir padding de 2 pixeles
img_padding = np.zeros((altura + 4, ancho + 4, canales), dtype=np.uint8)

"""
altura + 4: Ya que se añaden 2 pixeles arriba y 2 abajo
ancho + 4: Ya que se añaden 2 pixeles a la izquierda y 2 a la derecha
canales: Los canales de la imagen (RGB)
"""

# Copiar la imagen original en el centro de la nueva imagen con padding
img_padding[2:-2, 2:-2, :] = img

# Colorear el padding del color del pixel más cercano
for i in range(2):
    img_padding[i, 2:-2, :] = img[0, :, :]
    img_padding[-i-1, 2:-2, :] = img[-1, :, :]
    img_padding[2:-2, i, :] = img[:, 0, :]
    img_padding[2:-2, -i-1, :] = img[:, -1, :]

# Guardar imagen con padding
Image.fromarray(img_padding).save('nueva_imagen.jpg')