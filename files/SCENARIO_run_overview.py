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
    
    scenario_1 = Simulated_Scenario()
    scenario_1.process_all_AVs()
    scenario_1.process_all_obs()
    # util_vsb.save_test(scenario_1.array_AVs,scenario_1.obs_array, scenario_1.intersection)
    scenario_1.to_excel()
    
    scenario_1.simulate_broadcast_communication()
    scenario_1.simulate_naive_communication()
    scenario_1.simulate_optimized_communication()
    
    #scenario_1.plot_communication_stats('data/content_communication_broadcast.xlsx', 'data/content_communication_naive.xlsx', 'data/content_communication_mex_counts_optimize.xlsx')
    
    #scenario_1.find_min_distance_directions()
    #scenario_1.find_min_distance_and_construct_obstacle_dictionary()


    #scenario_1.evaluate_obstacles_visibility_dir()
    
        
    # scenario_1.to_excel_with_messages()
    # scenario_1.to_excel_with_single_messages()
    
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
