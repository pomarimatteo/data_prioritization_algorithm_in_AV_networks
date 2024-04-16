import numpy as np
import matplotlib.pyplot as plt
import math
import os
import tikzplotlib


class Functions:
    
    @staticmethod
    def proximity_relation_strength_function(x, d0, k):
        # Logistic function for proximity_relation_strength
        return 1 - 1 / (1 + np.exp(-k * (x - d0)))

    #plot
    
    @staticmethod
    def tikzplotlib_fix_ncols(obj):
        if hasattr(obj, "_ncols"):
            obj._ncol = obj._ncols
        for child in obj.get_children():
            Functions.tikzplotlib_fix_ncols(child)

    
    @staticmethod
    def plot_proximity_relation_strength(array_d0=25, k=0.5):
        # Plot the proximity_relation_strength function
        x_values = np.linspace(0, 100, 1000)
        d1 = 80
        array_d0 = [array_d0]
        plt.figure(figsize=(15, 9))

        for d0 in array_d0:
            y_values = Functions.proximity_relation_strength_function(x_values, d0, k)

            plt.plot(x_values, y_values, label=f'Proximity Relation Strength Function (d0={d0}, k={k})', linewidth=2)
            plt.axvline(x=d0, color='gray', linestyle='-', linewidth=0.8)
            plt.axvline(x=d1, color='gray', linestyle='-', linewidth=0.8)
            plt.fill_betweenx(y_values, d0, d1, color='lightgray', alpha=0.5)
            plt.fill_betweenx(y_values, d1, 100, color='dimgray', alpha=0.5)
            plt.text((d0 + d1) / 2, 0.5, 'Ineffective', color='black', rotation=90, ha='center', va='center')
            plt.text(d1 + 10, 0.5, 'Out of range', color='black', rotation=90, ha='center', va='center')

        plt.title('Proximity Relation Strength', fontsize=24)  # Modifica dimensione carattere titolo
        plt.xlabel('$x$', fontsize=28)  # Modifica dimensione carattere asse x
        plt.ylabel('$f(x)$', fontsize=28)  # Modifica dimensione carattere asse y
        
        
        plt.grid(False)
        plt.legend(title='Legend', title_fontsize='20', loc='upper right', fontsize=14)  # Modifica dimensione carattere legenda
        
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
        
        plt.xlim(0, 110)
        plt.ylim([0, 1])
        
        Functions.tikzplotlib_fix_ncols(plt.gcf())  # Chiamata a tikzplotlib_fix_ncols prima di salvare il grafico
        tikzplotlib.save("__plot.tex")
        
        plt.show()



Functions.plot_proximity_relation_strength(25,0.5)
