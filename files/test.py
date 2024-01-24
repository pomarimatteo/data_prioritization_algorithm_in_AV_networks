from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater
from SELMA_frames_file_handler import FramesFileHandler
from AHP import AHP
from AHP_conditional_VOI import Conditional_VOI
import matplotlib.pyplot as plt
import random


from utility import Utility as util
from util_visibility import Util_visibility as util_vsb

import geopandas as gpd 

class Test:
    '''
    # Esempio di utilizzo:
    file_handler = FramesFileHandler('data/segmentation/sc_01/filtered_segmentation.json')
    counts_by_type = file_handler.group_objects_by_type()

    file_handler.print_grouped_by_type(counts_by_type)
    ###
    
    print('group_objects_by_type_dist \n')
    counts_by_type_dist = file_handler.group_objects_by_type_dist()
    file_handler.print_grouped_by_type(counts_by_type_dist)
    
    '''
    
    a = 9  # ('Novelty', 'Reliability')
    b = 3  # ('Novelty', 'Distance')
    c = 3  # ('Novelty', 'Content')
    d = 1/6  # ('Reliability', 'Distance')
    e = 1/8  # ('Reliability', 'Content')
    f = 1  # ('Distance', 'Content')

    
    
    matrix = {
        
        ('Novelty', 'Novelty'): 1,
        ('Novelty', 'Reliability'): a,
        ('Novelty', 'Distance'): b,
        ('Novelty', 'Content'): c,

        ('Reliability', 'Novelty'): 1/a,
        ('Reliability', 'Reliability'): 1,
        ('Reliability', 'Distance'): d,
        ('Reliability', 'Content'): e,

        ('Distance', 'Novelty'): 1/b,
        ('Distance', 'Reliability'): 1/d,
        ('Distance', 'Distance'): 1,
        ('Distance', 'Content'): f,

        ('Content', 'Novelty'): 1/c,
        ('Content', 'Reliability'): 1/e,
        ('Content', 'Distance'): 1/f,
        ('Content', 'Content'): 1,
    }
    
    
    ahp_calculator = AHP(matrix)

    print(ahp_calculator.get_weights())
    print('\n')
    print(ahp_calculator.get_consistency_ratio())
    #ahp_calculator.print_report()
    
    conditional_VOI = Conditional_VOI(ahp_calculator)
    values = [5,5,5,0.8]
    print(conditional_VOI.calculate_importance_value(values))
    
    # Liste per memorizzare i valori di i e i corrispondenti risultati della funzione
    i_values = []
    result_values = []

    for i in range(60):
        values = [15, i, 15, 0.8]
        
        # Stampare il vettore values
        print("Vettore values:", values)
        
        # Stampare il risultato della funzione calculate_importance_value
        result = conditional_VOI.calculate_importance_value(values)
        #print("Risultato della funzione:", result)
        #print()
        
        # Aggiungere i valori alle liste
        i_values.append(i)
        result_values.append(result)

    # Plot dell'andamento
    plt.plot(i_values, result_values, marker='o')
    plt.title('Trend')
    plt.xlabel('i value')
    plt.ylabel('Results')
    plt.show()
    



Test()






