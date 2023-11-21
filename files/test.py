from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater
from frames_file_handler import FramesFileHandler

from utility import Utility as util
from util_visibility import Util_visibility as util_vsb

import geopandas as gpd 

class Test:

    # Esempio di utilizzo:
    file_handler = FramesFileHandler('data/segmentation/sc_01/filtered_segmentation.json')
    counts_by_type = file_handler.group_objects_by_type()

    file_handler.print_grouped_by_type(counts_by_type)
    ###
    
    file_handler.draw_rectangle_mask('left_sc_01.jpg288635')


    
Test()






