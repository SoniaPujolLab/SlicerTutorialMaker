import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
from PIL import Image


img = np.asarray(Image.open('Resources/Images/-20230523-182017.png'))
#print(repr(img))
imgplot = plt.imshow(img)

# Agregar Textos
plt.annotate('Anotación en texto', xy=(20, 40), xytext=(250, 480), color='#FFFFFF')

# Agregar flechas
plt.annotate('', xy=(150, 200), xytext=(150, 350), arrowprops=dict(arrowstyle='->', color='#FF0000'))
plt.annotate('', xy=(500, 500), xytext=(400, 800), arrowprops=dict(arrowstyle='-|>', color='yellow'))

# Agregar rectángulos
rect = patches.Rectangle((1000, 300), 200, 150, edgecolor='red', facecolor='none')
plt.gca().add_patch(rect)

# Agregar círculos
circle = patches.Circle((750, 850), 100, edgecolor='blue', facecolor='none')
plt.gca().add_patch(circle)


plt.title('Imagen con Anotaciones')
plt.axis('off')
plt.show()