import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.patches as patches
import numpy as np
from PIL import Image
import json


with open("metadata_test.json", "r") as file:
    data = json.load(file)

print(data)


img = np.asarray(Image.open('Resources/Images/-20230523-182017.png'))
#print(repr(img))
imgplot = plt.imshow(img)

# Enmarcar en componente
x,y = data[0]['position']
w, h = data[0]['size']
rect = patches.Rectangle((x, y), w, h, edgecolor='red', facecolor='none')
plt.gca().add_patch(rect)

# Agregar una flecha
long = 200
plt.annotate('', xy=(x+w,y+(h/2)), xytext=(x+w+long,y+(h/2)), arrowprops=dict(arrowstyle='->', color='#FF0000'))

# Agregar Textos
plt.annotate(data[0]['widget'], xy=(0,0), xytext=(x+w+long, y+(h/2)), color='#FF0000')



plt.title(data[0]['step'])
plt.axis('off')
plt.show()