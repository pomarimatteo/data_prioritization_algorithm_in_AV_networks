import numpy as np
import matplotlib.pyplot as plt
import math

class Functions:

    @staticmethod
    def proximity_relation_strength_function(x, d0, k):
        # Logistic function for proximity_relation_strength
        return 1 - 1 / (1 + np.exp(-k * (x - d0)))

    @staticmethod
    def n_obstacles_function(n, k, n_max):
        # Function to compute object importance based on the number of obstacles
        return (1 - math.exp(-n / k)) / (1 - math.exp(-n_max / k))

    @staticmethod
    def proximity_function(x, d0, k):
        # Proximity function indicating closeness to a point
        return 1 - 1 / (1 + np.exp(-k * (x - d0)))

    @staticmethod
    def accuracy_function(x):
        # Piecewise accuracy function
        if 0 <= x < 0.3:
            return 0
        elif 0.3 <= x <= 1:
            return 1
        else:
            return 1  # Default value for x outside the specified range


    @staticmethod
    def plot_proximity_relation_strength(array_d0, k):
        # Plot the proximity_relation_strength function
        x_values = np.linspace(0, 100, 100)
        d1 = 80
        array_d0 = [array_d0]
        plt.figure(figsize=(10, 6))

        for d0 in array_d0:
            y_values = Functions.proximity_relation_strength_function(x_values, d0, k)

            plt.plot(x_values, y_values, label=f'Proximity Relation Strength Function (d0={d0}, k={k})', linewidth=2)
            plt.axvline(x=d0, color='gray', linestyle='--', linewidth=0.8)
            plt.axvline(x=d1, color='gray', linestyle='--', linewidth=0.8)
            plt.fill_betweenx(y_values, d0, d1, color='darkgray', alpha=0.5)
            plt.fill_betweenx(y_values, d1, 100, color='dimgray', alpha=0.5)
            plt.text((d0 + d1) / 2, 0.5, 'Ineffective', color='black', rotation=90, ha='center', va='center')
            plt.text(d1 + 10, 0.5, 'Out of range', color='black', rotation=90, ha='center', va='center')

        plt.title('Proximity Relation Strength')
        plt.xlabel('$x$')
        plt.ylabel('$f(x)$')
        plt.grid(False)
        plt.legend(title='Legend', title_fontsize='14', loc='upper right')
        plt.xlim(0, 110)
        plt.ylim([0, 1])
        plt.show()

    @staticmethod
    def plot_n_obstacles_function(k, n_max):
        # Plot the object importance function
        n_values = np.arange(0, 25, 1)
        importance_values = [Functions.n_obstacles_function(n, k, n_max) for n in n_values]

        plt.figure(figsize=(8, 6))
        plt.plot(n_values, importance_values, label='Object Importance')
        plt.axhline(y=1, color='black', linestyle='--', label='Asymptote at y=1')
        plt.xlabel('n')
        plt.ylabel('Image Importance')
        plt.title('Objects')
        plt.legend()
        plt.show()

    @staticmethod
    def plot_proximity_function(d0, k):
        # Plot the proximity function
        x_values = np.linspace(0, 200, 100)
        y_values = Functions.proximity_function(x_values, d0, k)

        plt.figure(figsize=(8, 6))
        plt.plot(x_values, y_values, label=f'Proximity Function (d0={d0}, k={k})')
        plt.title('Proximity Function')
        plt.xlabel('x')
        plt.ylabel('Proximity')
        plt.legend()
        plt.show()

    @staticmethod
    def plot_accuracy_function():
        # Plot the accuracy function
        x_values = np.linspace(0, 1.5, 10)
        y_values = [Functions.accuracy_function(x) for x in x_values]

        plt.plot(x_values, y_values, label='Accuracy Function: $y = 1$')
        plt.xlabel('x')
        plt.title('Accuracy Function Plot')
        plt.legend()
        plt.show()

# usage
'''
Functions.plot_proximity_relation_strength(20,0.5)
Functions.plot_n_obstacles_function(0.5,10)
Functions.plot_proximity_function(50,0.5)
Functions.plot_accuracy_function()
'''