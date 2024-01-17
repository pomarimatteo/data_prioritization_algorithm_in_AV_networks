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

# **************************************************** #
    
    # 1) generate n random AVs
    
    # 2) generate m random obstacles
    
    # 3) verify each obstacle in every LoS
    
    # 4) evaluate the broadcast communication
    
    # 5) implement consideration and AHP for prioritarization of the data
    
    # 6) evaluate the new communication
    
# **************************************************** #


class SCENARIO_run:
    
    # generate target AV
    my_car_map = ss.generate_myself()
    
    # generate other Avs
    other_AVs = ss.generate_AVs()
    
    # retrive info about other AVs
    ss.detect_other_AVs(my_car_map, other_AVs)
    
    util_vsb.show_visibility_graph_multiple_cars(my_car_map.car, other_AVs, ss.intersection)
    my_car_map.car.print_car_info()
    
    

    

        
        
        
        
        
        
     
        

    
    
    
    
    
    
    