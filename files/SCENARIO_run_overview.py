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
    
    '''
    # SCENARIO 1
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
        ('D', 11.007484262837124, 45.43954676351245, 0.1),
        ('E', 11.008225211533869, 45.43960992760452, 180),
        ('F', 11.007983298078727, 45.439737059970014, 270)
    ]
    n_obs = 4
    intersection = gpd.read_file('data/geojson/map_001.geojson')
    road = gpd.read_file('data/geojson/road.geojson')

    scenario_1 = Simulated_Scenario(polygon_spawn, car_data, n_obs, intersection, road)
    '''
    
    scenario_1 = Simulated_Scenario()
    scenario_1.process_all_AVs()
    scenario_1.process_all_obs()
    #util_vsb.save_test(scenario_1.array_AVs,scenario_1.obs_array, scenario_1.intersection)
    scenario_1.to_excel()
    
    scenario_1.simulate_broadcast_communication()
    scenario_1.simulate_naive_communication()
    #scenario_1.simulate_optimized_communication()
    
    scenario_1.optimized_method()
    
    '''
    b = []
    n = []
    o = []

    for i in range(20):
        scenario_1 = Simulated_Scenario()
        scenario_1.process_all_AVs()
        scenario_1.process_all_obs()
        
        result_b = scenario_1.simulate_broadcast_communication()
        b.append(result_b)
        
        result_n = scenario_1.simulate_naive_communication()
        n.append(result_n)
        
        result_o = scenario_1.simulate_optimized_communication()
        o.append(result_o)

    # Organizzazione dei dati in una lista di dizionari per b
    data_rows_b = []
    for result in b:
        data_rows_b.append({
            "total_messages_sent": result["total_messages_sent"],
            "average_dist": result["average_dist"],
            "redundancy_count": result["redundancy_count"],
            "redundancy_perc": result["redundancy_perc"]
        })

    # Creazione del DataFrame pandas per b
    df_b = pd.DataFrame(data_rows_b)

    # Salvataggio su Excel per b
    df_b.to_excel("data/_broadcast_simulation.xlsx", index=False)

    # Organizzazione dei dati in una lista di dizionari per n
    data_rows_n = []
    for result in n:
        data_rows_n.append({
            "total_messages_sent": result["total_messages_sent"],
            "average_dist": result["average_dist"],
            "redundancy_count": result["redundancy_count"],
            "redundancy_perc": result["redundancy_perc"]
        })

    # Creazione del DataFrame pandas per n
    df_n = pd.DataFrame(data_rows_n)

    # Salvataggio su Excel per n
    df_n.to_excel("data/_naive_simulation.xlsx", index=False)

    # Organizzazione dei dati in una lista di dizionari per o
    data_rows_o = []
    for result in o:
        data_rows_o.append({
            "total_messages_sent": result["total_messages_sent"],
            "average_dist": result["average_dist"],
            "redundancy_count": result["redundancy_count"],
            "redundancy_perc": result["redundancy_perc"]
        })

    # Creazione del DataFrame pandas per o
    df_o = pd.DataFrame(data_rows_o)

    # Salvataggio su Excel per o
    df_o.to_excel("data/_optimized_simulation.xlsx", index=False)



    
    
    #scenario_1.save_data_simulation()

    
    
    #scenario_1.plot_communication_stats('data/content_communication_broadcast.xlsx', 'data/content_communication_naive.xlsx', 'data/content_communication_mex_counts_optimize.xlsx')
    
    #scenario_1.find_min_distance_directions()
    #scenario_1.find_min_distance_and_construct_obstacle_dictionary()


    #scenario_1.evaluate_obstacles_visibility_dir()
    
        
    # scenario_1.to_excel_with_messages()
    # scenario_1.to_excel_with_single_messages()
    
    '''
    
    '''
    
    scenario_1.evaluate_obstacles_visibility()
        
    scenario_1.print_tabular_table()
    
    print('\nevaluate_obstacles_visibility\n')
    scenario_1.evaluate_obstacles_visibility()
    scenario_1.evaluate_obstacles_visibility_plot()
    print('\nevaluate_obstacles_visibility_dir\n')
    scenario_1.evaluate_obstacles_visibility_dir()
    scenario_1.print_obstacles_visibility_info()
    #scenario_1.plot_obstacles_visibility_heatmap()
    
    scenario_1.simulate_communication_uni()


    #scenario_1.voi()
    Functions.save_all_plots()
    '''