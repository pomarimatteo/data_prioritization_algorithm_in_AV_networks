from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater
from OBS import Obstacle
from OBS_in_map import OBS_in_map
from UTIL_data import Data
from SCENARIO_method import Simulated_Scenario
from AHP import AHP
from AHP_conditional_VOI import Conditional_VOI
from AHP_functions import Functions
import seaborn as sns
import math
import numpy as np
from tqdm import tqdm  #
from mpl_toolkits.mplot3d import Axes3D



from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from utility import Utility as util
from util_visibility import Util_visibility as util_vsb
from shapely.geometry import Point
from tabulate import tabulate
import random
import pandas as pd
import geopandas as gpd 

class Class:
    
    # **************************************************** #
    # 1) generate n random AVs
    # 2) generate m random obstacles
    # 3) verify each obstacle in every LoS
    # 4) evaluate the broadcast communication
    # 5) implement consideration and AHP for prioritization of the data
    # 6) evaluate the new communication
    # **************************************************** #
    
    '''
    * IMPORTANT
    * i seguenti metodi devono essere chiamati
    * valuta di inserirli all'interno dei simulate_communication
    '''
    
    # SCENARIO 1
    geojson_path = 'data/geojson/'
    
    # Inizializza i dataframe per i dati di ogni simulazione
    broadcast_data = pd.DataFrame(columns=['total_messages_sent', 'average_dist', 'redundancy_count', 'redundancy_perc'])
    naive_data = pd.DataFrame(columns=['total_messages_sent', 'average_dist', 'redundancy_count', 'redundancy_perc'])
    optimized_data = pd.DataFrame(columns=['total_messages_sent', 'average_dist', 'redundancy_count', 'redundancy_perc'])
     
    intersection = gpd.read_file(geojson_path + 'map_001.geojson')
    road = gpd.read_file(geojson_path + 'road.geojson')
    
    n_car = 5
    #intersection = gpd.read_file(geojson_path + 'map_003.geojson')
    #road = gpd.read_file(geojson_path + 'road_003.geojson')
    
    #urban
    polygon_spawn = [
        [11.0069841, 45.4395318],
        [11.0069716, 45.4394266],
        [11.0077328, 45.4395250],
        [11.0077888, 45.4393060],
        [11.0078187, 45.4393031],
        [11.0077820, 45.4395357],
        [11.0086243, 45.4395781],
        [11.0085992, 45.4396572]
    ]
    '''
    # milano
    polygon_spawn = [
        [9.101358, 45.436413],
        [9.10157,45.43636],
        [9.105369, 45.437639],
        [9.10637, 45.436012],
        [9.106918, 45.435943],
        [9.10563, 45.437961],
        [9.109259, 45.439145],
        [9.109093, 45.439562],
        [9.105708, 45.438562],
        [9.103633, 45.43943],
        [9.10402, 45.439824],
        [9.105021, 45.438231]
    ]
    
    #velo
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
    '''
   
    
    car_data = [
        ('A', 11.007767285707814, 45.439492436628484, 90),
        ('B', 11.007789421555742, 45.43937903284822, 90),
        ('C', 11.007903263242582, 45.439586043947855, 180),
        ('D', 11.007484262837124, 45.43954676351245, 0.1),
        ('E', 11.008225211533869, 45.43960992760452, 180),
        ('F', 11.007983298078727, 45.439737059970014, 270)
    ]
    
    obs_data = [
        ('obs01', 11.007994965432141, 45.43956251307974),
        ('obs02', 11.007259879567288, 45.439501301102375),
        ('obs03', 11.007524314620381, 45.43957334519733),
        ('obs04', 11.00811932397948, 45.43955290255859),
        ('obs05', 11.007794071474587, 45.43945523711499),
        ('obs06', 11.008327864869, 45.43958895589447),
        ('obs07', 11.007239494837371, 45.43954782572268),
        ('obs08', 11.007182339769145, 45.439518758415836),
        ('obs09', 11.007204585265388, 45.43954086015715),
        ('obs10', 11.007758, 45.439571),
        #('obs11', 11.007759, 45.439571)
    ]

    # Definisci i valori di n_cars e n_obs su cui iterare
    n_cars_values = [3, 5, 6]
    n_obs_values = [10, 15, 20, 25, 30, 40]

    # Inizializza le liste per salvare i risultati
    total_messages_broadcast = []
    total_messages_naive = []
    total_messages_optimized = []
    redundancy_percentage_broadcast = []
    redundancy_percentage_naive = []
    redundancy_percentage_optimized = []

    # Calcola i total messages per ogni valore di n_obs e metodo
    for n_cars in n_cars_values:
        for n_obs in n_obs_values:
            # Esegui la simulazione per il valore corrente di n_obs
            broadcast_data = pd.DataFrame(columns=['total_messages_sent', 'average_dist', 'redundancy_count', 'redundancy_perc'])
            naive_data = pd.DataFrame(columns=['total_messages_sent', 'average_dist', 'redundancy_count', 'redundancy_perc'])
            optimized_data = pd.DataFrame(columns=['total_messages_sent', 'average_dist', 'redundancy_count', 'redundancy_perc'])
            
            for i in tqdm(range(100), desc=f"Simulazione per n_cars = {n_cars}, n_obs = {n_obs}"):
                array_AVs = Simulated_Scenario.generate_AVs(n_cars, polygon_spawn)
                obs_array = Simulated_Scenario.generate_obstacles(n_obs, polygon_spawn)
                
                scenario = Simulated_Scenario(array_AVs, obs_array, intersection, road)
                scenario.process_all_AVs()
                scenario.process_all_obs()
                
                broadcast_results = scenario.simulate_broadcast_communication()
                naive_results = scenario.simulate_naive_communication()
                optimized_results = scenario.optimized_method()
                
                broadcast_data.loc[i] = broadcast_results
                naive_data.loc[i] = naive_results
                optimized_data.loc[i] = optimized_results
            
            # Calcola la media dei total messages e percentuale di ridondanza per ogni metodo
            total_messages_broadcast.append(broadcast_data['total_messages_sent'].mean())
            total_messages_naive.append(naive_data['total_messages_sent'].mean())
            total_messages_optimized.append(optimized_data['total_messages_sent'].mean())
            
            redundancy_percentage_broadcast.append(broadcast_data['redundancy_perc'].mean())
            redundancy_percentage_naive.append(naive_data['redundancy_perc'].mean())
            redundancy_percentage_optimized.append(optimized_data['redundancy_perc'].mean())




    # Define the values of n_cars and n_obs
    n_cars_values = [3, 5,  7]
    n_obs_values = [10, 15, 20, 25, 30,35]

    # Define line styles for different values of n_cars
    line_styles = [':', '-.', '-']

    # Define a color palette of slightly darker gray shades
    colors = ['#b2b2b2', '#999999', '#7f7f7f', '#666666', '#4d4d4d']
    colors = ['blue', "#22a7f0", "#a7d5ed"]

    # Plot for the optimized method
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.title('Optimized Method - Total Messages Sent')
    plt.xlabel('Number of Obstacles (n_obs)')
    plt.ylabel('Message count')
    for i, n_cars in enumerate(n_cars_values):
        plt.plot(n_obs_values, total_messages_optimized[i*len(n_obs_values):(i+1)*len(n_obs_values)], linestyle=line_styles[i], label=f'n_cars={n_cars}', color=colors[i])
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.title('Optimized Method - Redundancy Percentage')
    plt.xlabel('Number of Obstacles (n_obs)')
    plt.ylabel('Redundancy')
    for i, n_cars in enumerate(n_cars_values):
        plt.plot(n_obs_values, redundancy_percentage_optimized[i*len(n_obs_values):(i+1)*len(n_obs_values)], linestyle=line_styles[i], label=f'n_cars={n_cars}', color=colors[i])
    plt.legend()

    plt.tight_layout()
    plt.show()