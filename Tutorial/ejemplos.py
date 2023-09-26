def calcular_pendiente(x1, y1, x2, y2):
    # Calcula la diferencia en las coordenadas x e y
    dx = x2 - x1
    dy = y2 - y1

    # Calcula la pendiente
    pendiente = dy / dx

    return pendiente

# Ejemplo de uso
x1 = 1
y1 = 1
x2 = 2
y2 = 2

pendiente = calcular_pendiente(x1, y1, x2, y2)
print("La pendiente entre los puntos ({}, {}) y ({}, {}) es: {}".format(x1, y1, x2, y2, pendiente))


x1 = -1
y1 = 1
x2 = -2
y2 = 2

pendiente = calcular_pendiente(x1, y1, x2, y2)
print("La pendiente entre los puntos ({}, {}) y ({}, {}) es: {}".format(x1, y1, x2, y2, pendiente))

x1 = -1
y1 = -1
x2 = -2
y2 = -2

pendiente = calcular_pendiente(x1, y1, x2, y2)
print("La pendiente entre los puntos ({}, {}) y ({}, {}) es: {}".format(x1, y1, x2, y2, pendiente))


x1 = 1
y1 = -1
x2 = 2
y2 = -2

pendiente = calcular_pendiente(x1, y1, x2, y2)
print("La pendiente entre los puntos ({}, {}) y ({}, {}) es: {}".format(x1, y1, x2, y2, pendiente))
