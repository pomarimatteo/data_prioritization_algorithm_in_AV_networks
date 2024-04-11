import numpy as np
import matplotlib.pyplot as plt

def logistic_function(x, k, x0):
    return 1 / (1 + np.exp(-k * (x - x0)))

# Definizione dei parametri
k = 1.0
x0 = 10.0

# Generazione di dati x
x_values = np.linspace(0, 20, 1000)

# Calcolo dei valori della funzione
y_values = logistic_function(x_values, k, x0)

# Plot della funzione
plt.plot(x_values, y_values)
plt.title('Logistic Function')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.show()
