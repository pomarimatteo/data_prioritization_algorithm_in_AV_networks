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
import numpy as np

from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from utility import Utility as util
from util_visibility import Util_visibility as util_vsb
from shapely.geometry import Point
from tabulate import tabulate
import random
import pandas as pd
import geopandas as gpd 


class SCENARIO_run_overview:
    
    # **************************************************** #
     # 1) generate n random AVs
     
     # 2) generate m random obstacles
     
     # 3) verify each obstacle in every LoS
     
     # 4) evaluate the broadcast communi cation
      
     # 5) implement consideration and AHP for prioritarization of the data
     
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
    
    car_data = [
        ('A', 11.007767285707814, 45.439492436628484, 90),
        ('B', 11.007789421555742, 45.43937903284822, 90),
        ('C', 11.007903263242582, 45.439586043947855, 180),
        #('D', 11.007484262837124, 45.43954676351245, 0.1),
        #('E', 11.008225211533869, 45.43960992760452, 180),
        #('F', 11.007983298078727, 45.439737059970014, 270)
    ]
   
   
    #n_obs_intervals = [(0, 10), (10, 20), (20, 30)]

    #for n_obs_interval in n_obs_intervals:
        # Esegui il loop per ogni intervallo
    for i in range(1):   
        print(i)  

        
        n_car = random.randint(1, 15)
        n_car = 5
        n_obs = random.randint(10, 12)
        
        n_obs = 15
        
        array_AVs = Simulated_Scenario.generate_AVs(n_car, polygon_spawn)
        obs_array = Simulated_Scenario.generate_obstacles(n_obs, polygon_spawn)
        
        scenario = Simulated_Scenario(car_data, obs_array, intersection, road)
        #scenario = Simulated_Scenario(array_AVs, obs_array, intersection, road)
                
        scenario.process_all_AVs()
        scenario.process_all_obs()

        
        util_vsb.save_test(scenario.array_AVs,scenario.obs_array, scenario.intersection)
        scenario.to_excel()
        #util_vsb.show_visibility_graph_multiple_cars(scenario.array_AVs[0],scenario.array_AVs,scenario.obs_array, scenario.intersection)
        
        # Esegui le simulazioni
        #broadcast_results = scenario.simulate_broadcast_communication()
        #naive_results = scenario.simulate_naive_communication()
        #optimized_results = scenario.optimized_method()
        
        scenario.metodo()
        

        # Aggiungi i risultati alle rispettive dataframe
        #broadcast_data.loc[i] = broadcast_results
        #naive_data.loc[i] = naive_results
        #optimized_data.loc[i] = optimized_results
    
    
    
    #util
    '''
 
    # Salva i dataframe in file Excel
    broadcast_data.to_excel("broadcast_results.xlsx", index=False)
    naive_data.to_excel("naive_results.xlsx", index=False)
    optimized_data.to_excel("optimized_results.xlsx", index=False)    

    
    # Calcolo delle medie per i messaggi totali inviati
    broadcast_avg_total_messages = broadcast_data['total_messages_sent'].mean()
    naive_avg_total_messages = naive_data['total_messages_sent'].mean()
    optimized_avg_total_messages = optimized_data['total_messages_sent'].mean()
    
    # Calcolo delle medie per i messaggi di ridondanza
    broadcast_avg_redundancy_count = broadcast_data['redundancy_count'].mean()
    print('broadcast_avg_redundancy_count',broadcast_avg_redundancy_count)
    naive_avg_redundancy_count = naive_data['redundancy_count'].mean()
    optimized_avg_redundancy_count = optimized_data['redundancy_count'].mean()
    
    # Calcolo delle medie per i messaggi di ridondanza
    broadcast_average_dist = broadcast_data['average_dist'].mean()
    naive_avg_average_dist = naive_data['average_dist'].mean()
    optimized_average_distt = optimized_data['average_dist'].mean()
    
    # Calcolo delle medie per i messaggi di ridondanza
    broadcast_avg_redundancy_perc = broadcast_data['redundancy_perc'].mean()
    naive_avg_redundancy_perc = naive_data['redundancy_perc'].mean()
    optimized_avg_redundancy_perc = optimized_data['redundancy_perc'].mean()
    
    # Dati dei messaggi totali inviati
    labels = ['Broadcast', 'Naive', 'Optimized']
    avg_total_messages = [broadcast_avg_total_messages, naive_avg_total_messages, optimized_avg_total_messages]

    # Dati della distanza media
    avg_distance = [broadcast_average_dist, naive_avg_average_dist, optimized_average_distt]
    
    avg_redundancy = [broadcast_avg_redundancy_count, naive_avg_redundancy_count,optimized_avg_redundancy_count]
    
    # Dati della distanza media
    avg_distance = [broadcast_average_dist, naive_avg_average_dist, optimized_average_distt]


    labels = ['Broadcast', 'Naive', 'Optimized']

    


    # Plot
    fig, ax1= plt.subplots()

    color = 'grey'  # Colori modificati
    ax1.set_xlabel('Communication Type')
    ax1.set_ylabel('Average Total Messages Sent')
    ax1.bar(labels, avg_total_messages, color=color, width=0.45)  # Larghezza delle barre modificata
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()
    color = 'tab:orange'  # Colori modificati
    ax2.set_ylabel('Average Distance')
    ax2.plot(labels, avg_distance, color=color,linestyle='--', marker='o')
    ax2.tick_params(axis='y', labelcolor=color)
    
    # Sovrapposizione dei dati sulla ridondanza
    #ax3 = ax1.twinx()
    
    hatch_pattern = '///'
    color = 'red'
    #ax3.set_ylabel('Average Redundancy Count', color=color)
    ax1.bar(labels, avg_redundancy, color=color, width=0.45, hatch=hatch_pattern, alpha=1)  # Larghezza delle barre modificata
    ax1.tick_params(axis='y', labelcolor=color)

    


    max_y = max(avg_distance)
    ax2.set_ylim(0, max_y * 3/2)  
    
    # Personalizzazione degli spazi tra le tick sull'asse x
    ax1.set_xticks(np.arange(len(labels)))
    ax1.set_xticklabels(labels)
    
    
    fig.tight_layout()
    plt.title('Average Total Messages Sent vs Average Distance vs Average Redundancy Count')
    plt.show()
    
    '''
    
    
    
    
    
    
    
    '''
    # Dati per i tipi di comunicazione
    communication_methods = ['Broadcast', 'Naive', 'Optimized']

    # Medie dei messaggi totali inviati
    total_messages_avg = [broadcast_avg_total_messages, naive_avg_total_messages, optimized_avg_total_messages]


    
    plt.figure(figsize=(10, 6))
    plt.bar(communication_methods, total_messages_avg, color=['orange', 'grey', 'green'])
    plt.title('Media dei messaggi totali inviati per tipo di comunicazione')
    plt.xlabel('Tipo di comunicazione')
    plt.ylabel('Media dei messaggi totali inviati')
    plt.show()





    
    # Medie per i messaggi di ridondanza
    redundancy_count_avg = [broadcast_avg_redundancy_count, naive_avg_redundancy_count, optimized_avg_redundancy_count]

    plt.figure(figsize=(10, 6))
    plt.bar(communication_methods, redundancy_count_avg, color=['blue', 'green', 'red'])
    plt.title('Media dei messaggi di ridondanza per tipo di comunicazione')
    plt.xlabel('Tipo di comunicazione')
    plt.ylabel('Media dei messaggi di ridondanza')
    plt.show()

    # Medie per la distanza media dei messaggi
    average_dist_avg = [broadcast_average_dist, naive_avg_average_dist, optimized_average_distt]

    plt.figure(figsize=(10, 6))
    plt.bar(communication_methods, average_dist_avg, color=['blue', 'green', 'red'])
    plt.title('Media della distanza media dei messaggi per tipo di comunicazione')
    plt.xlabel('Tipo di comunicazione')
    plt.ylabel('Media della distanza media dei messaggi')
    plt.show()

    # Medie per la percentuale di ridondanza dei messaggi
    redundancy_perc_avg = [broadcast_avg_redundancy_perc, naive_avg_redundancy_perc, optimized_avg_redundancy_perc]

    plt.figure(figsize=(10, 6))
    plt.bar(communication_methods, redundancy_perc_avg, color=['blue', 'green', 'red'])
    plt.title('Media della percentuale di ridondanza dei messaggi per tipo di comunicazione')
    plt.xlabel('Tipo di comunicazione')
    plt.ylabel('Media della percentuale di ridondanza dei messaggi')
    plt.show()
    '''
