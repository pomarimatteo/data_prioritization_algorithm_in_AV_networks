from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater
from OBS import Obstacle
from OBS_in_map import OBS_in_map
from UTIL_data import Data
from SCENARIO_method import Simulated_Scenario as ss

from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from utility import Utility as util
from util_visibility import Util_visibility as util_vsb
from shapely.geometry import Point
import random

class SCENARIO_run_overview:
    
    array_AVs = ss.generate_all_AVs()
    
    array_car_map = ss.generate_all_car_map(array_AVs)
    
    ss.process_all_AVs(array_car_map)
    
    obs_array = ss.generate_obstacles(10)
                                      
    # ss.info_AV(array_AVs)
    
    # util_vsb.show_visibility_graph_multiple_cars(array_AVs[0], array_AVs, ss.intersection)
    
    obs_event = OBS_in_map(array_car_map[0],obs_array)

    
    for obs in obs_array:
        New_AV_updater(array_car_map[0], obs).process_detected_obj()
    
    array_AVs[0].print_obstacle_ids()
    
    obs_event.plot()

    
    

    
    
    