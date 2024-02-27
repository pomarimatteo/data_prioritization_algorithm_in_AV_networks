import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

polygon_spawn = [
    [11.093765, 45.604405],
    [11.093987, 45.604389],
    [11.094671, 45.604102],
    [11.094742, 45.604567],
    [11.095167, 45.604233],
    [11.095650, 45.604669],
    [11.095817, 45.604554],
    [11.095370, 45.604253],
    [11.094987, 45.603848],
    [11.095089, 45.603726],
    [11.095666, 45.603345],
    [11.095423, 45.603194],
    [11.094762, 45.603937]
]

# Estrai le coordinate x e y
x = [point[0] for point in polygon_spawn]
y = [point[1] for point in polygon_spawn]

# Aggiungi il primo punto alla fine per chiudere il poligono
x.append(x[0])
y.append(y[0])

# Plot del poligono
plt.figure()
plt.plot(x, y, marker='o')
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Poligono generato dai punti forniti')
plt.grid(True)
plt.show()