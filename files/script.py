from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater


from utility import Utility as util
from util_visibility import Util_visibility as util_vsb

import geopandas as gpd 

class Script:

    # generation local map
    ##########################################
    # generate myself
    myself = Car('A', 11.007767285707814, 45.439492436628484, 90)

    # import geojson files
    intersection = gpd.read_file('data/intersection.geojson')
    road = gpd.read_file('data/road.geojson')
    map = (Map(intersection, road))

    # generate mymap
    my_car_map = My_car_map(myself,map)
    ##########################################



    # Create other AV cars
    other_cars = []
    car_data = [
        ('B', 11.007789421555742, 45.43937903284822, 90),
        ('C', 11.007903263242582, 45.439586043947855, 90),
        ('D', 11.007484262837124, 45.43954676351245, 90),
        ('E', 11.008225211533869, 45.43960992760452, 90),
        ('F', 11.007983298078727, 45.439737059970014, 90)]


    for ID, x, y, orientation in car_data:
        other_cars.append(Car(ID, x, y, orientation))

    #util_vsb.show_visibility_graph_multiple_cars(myself, other_cars, intersection)

    event_1 = New_AV_updater(my_car_map, other_cars[0])
    #event_1.show()
    event_1.add_car_camera_list()

    event_2 = New_AV_updater(my_car_map, other_cars[1])
    #event_2.show()
    event_2.add_car_camera_list()

    event_3 = New_AV_updater(my_car_map, other_cars[2])
    #event_3.show()
    event_3.add_car_camera_list()

    event_4 = New_AV_updater(my_car_map, other_cars[3])
    #event_4.show()
    event_4.add_car_camera_list()

    event_5 = New_AV_updater(my_car_map, other_cars[4])
    #event_5.show()
    event_5.add_car_camera_list()

    myself.print_car_info()

    Map_AV_updater(my_car_map, other_cars).show()
    util_vsb.show_visibility_graph_multiple_cars(myself, other_cars, intersection)

Script()










    




