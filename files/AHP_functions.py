import numpy as np
import matplotlib.pyplot as plt
import math
import os

class Functions:
    
    @staticmethod
    def roi_function(x):
        if x > 0 and x < 45:
            return 1 - 0.5 * (x / 45)
        elif x >= 45 and x < 135:
            return 0.5
        elif x >= 135:
            return 0.5 * np.exp(-0.02 * (x - 135))
        else:
            return None
    
    @staticmethod
    def proximity_relation_strength_function(x, d0, k):
        # Logistic function for proximity_relation_strength
        return 1 - 1 / (1 + np.exp(-k * (x - d0)))

    @staticmethod
    def n_obstacles_function(n, k, n_max):
        # Function to compute object importance based on the number of obstacles
        return (1 - math.exp(-n / k)) / (1 - math.exp(-n_max / k))

    #plot
    
    @staticmethod
    def plot_roi_function():
        x_values = np.linspace(0, 180, 1000)
        y_values = [Functions.roi_function(x) for x in x_values]

        plt.plot(x_values, y_values)
        plt.title('Funzione definita a tratti continua')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.show()
    
    @staticmethod
    def plot_proximity_relation_strength(array_d0=25, k=0.5):
        # Plot the proximity_relation_strength function
        x_values = np.linspace(0, 100, 1000)
        d1 = 80
        array_d0 = [array_d0]
        plt.figure(figsize=(10, 6))

        for d0 in array_d0:
            y_values = Functions.proximity_relation_strength_function(x_values, d0, k)

            plt.plot(x_values, y_values, label=f'Proximity Relation Strength Function (d0={d0}, k={k})', linewidth=2)
            plt.axvline(x=d0, color='gray', linestyle='--', linewidth=0.8)
            plt.axvline(x=d1, color='gray', linestyle='--', linewidth=0.8)
            plt.fill_betweenx(y_values, d0, d1, color='lightgray', alpha=0.5)
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
    def plot_n_obstacles_function(k=0.5, n_max=25):
        # Plot the object importance function
        #n_values = np.arange(0, 25, 1)
        n_values = np.linspace(0, 25, 100)
        importance_values = [Functions.n_obstacles_function(n, k, n_max) for n in n_values]

        plt.figure(figsize=(8, 6))
        plt.plot(n_values, importance_values, label='Object Importance')
        plt.axhline(y=1, color='black', linestyle='--', label='Asymptote at y=1')
        plt.xlabel('n')
        plt.ylabel('Image Importance')
        plt.title('Objects')
        plt.legend()
        plt.show()

    def save_all_plots():
        # Create a directory to save the plots
        save_dir = 'data/functions'
        os.makedirs(save_dir, exist_ok=True)

        # Save the plot for proximity_relation_strength_function
        Functions.plot_proximity_relation_strength(20, 0.5)
        plt.savefig(os.path.join(save_dir, 'proximity_relation_strength_plot.png'))
        plt.close()

        # Save the plot for n_obstacles_function
        Functions.plot_n_obstacles_function(0.5, 10)
        plt.savefig(os.path.join(save_dir, 'n_obstacles_function_plot.png'))
        plt.close()

        # Save the plot for proximity_function
        Functions.plot_proximity_function(50, 0.5)
        plt.savefig(os.path.join(save_dir, 'proximity_function_plot.png'))
        plt.close()

        # Save the plot for accuracy_function
        Functions.plot_accuracy_function()
        plt.savefig(os.path.join(save_dir, 'accuracy_function_plot.png'))
        plt.close()
# usage

'''
Functions.plot_roi_function()
Functions.plot_proximity_relation_strength(25,0.5)
Functions.plot_n_obstacles_function(5,25)
'''
#Functions.plot_n_obstacles_function(5,25)
