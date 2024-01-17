from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater
from OBS import Obstacle
from OBS_in_map import OBS_in_map
from UTIL_data import Data

from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from utility import Utility as util
from util_visibility import Util_visibility as util_vsb
from shapely.geometry import Point
import random

import geopandas as gpd 

class Script:

    # Define file paths as variables
    geojson_path = 'data/geojson/'

    # Define GPS coordinates as variables
    my_latitude = 11.007767285707814

    my_longitude = 45.439492436628484
    my_orientation = 90

    # Import geojson files
    intersection = gpd.read_file(geojson_path + 'map_001.geojson')
    road = gpd.read_file(geojson_path + 'road.geojson')

    other_cars = []
    car_data = [
        ('B', 11.007789421555742, 45.43937903284822, 90),
        ('C', 11.007903263242582, 45.439586043947855, 90),
        ('D', 11.007484262837124, 45.43954676351245, 90),
        ('E', 11.008225211533869, 45.43960992760452, 90),
        ('F', 11.007983298078727, 45.439737059970014, 90)]
    
    #obs_array = [Obstacle('obs001',11.007781900000000,45.439418600000000)]    

    
    # Create other AV cars
    for ID, x, y, orientation in car_data:
        other_cars.append(Car(ID, x, y, orientation))


    # GENERATE LOCAL MAP
    ##########################################
    # Generate myself
    myself = Car('A', my_latitude, my_longitude, my_orientation)

    # Generate map
    map = Map(intersection, road)

    # Generate my_car_map
    my_car_map = My_car_map(myself,map)
    ##########################################
    
    

    
    #util_vsb.show_visibility_graph_multiple_cars(myself, other_cars, intersection)

    event_1 = New_AV_updater(my_car_map, other_cars[0])
    event_1.process_detected_car()
    
    event_2 = New_AV_updater(my_car_map, other_cars[1])
    event_2.process_detected_car()
    
    #my_car_map.show()
    
    
    # OBSTACLES MANAGEMENT
    # n_obs = 5
    # obs_array = Data.generate_random_obstacles(my_car_map, n_obs)
    
    polygon_coords = [
        [11.0069841, 45.4395318],
        [11.0069716, 45.4394266],
        [11.0077328, 45.4395250],
        [11.0077888, 45.4393060],
        [11.0078187, 45.4393031],
        [11.0077820, 45.4395357],
        [11.0086243, 45.4395781],
        [11.0085992, 45.4396572]
    ]

    # Creazione del poligono
    polygon = Polygon(polygon_coords)

    # Generazione di 10 ostacoli casuali all'interno del poligono
    obstacle_data = []

    for i in range(10):
        # Generazione di un punto casuale all'interno del poligono
        while True:
            x = random.uniform(min(p[0] for p in polygon_coords), max(p[0] for p in polygon_coords))
            y = random.uniform(min(p[1] for p in polygon_coords), max(p[1] for p in polygon_coords))
            point = Point(x, y)
            
            # Verifica se il punto è all'interno del poligono
            if polygon.contains(point):
                break

        # Aggiunta dell'ostacolo alla lista
        obstacle_data.append(('obs{:02d}'.format(i + 1), x, y))
    
    
    obs_array = []
    
    for data in obstacle_data:
        obs = Obstacle(data[0], data[1], data[2])
        obs_array.append(obs)
    
    
    obs_event = OBS_in_map(my_car_map,obs_array)
    print(obs_event.obs_in_LoS())
    
    obs_event.plot()
    
    for obs in obs_array:
        New_AV_updater(my_car_map, obs).process_detected_obj()
    myself.print_obstacle_ids()

    
    #obs_event.print_cars_with_los()
    
    for other_car in other_cars:
        # Creare un evento per l'auto corrente
        event_other_car = New_AV_updater(my_car_map, other_car)
        
        # Eseguire le operazioni sull'auto corrente
        event_other_car.process_detected_car()
        
        # Stampare gli ID degli ostacoli dell'auto corrente
        other_car.print_obstacle_ids()
    

    # add other AVs
    '''
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

    '''

    #myself.print_car_info()

    #Map_AV_updater(my_car_map, other_cars).show()
    #util_vsb.show_visibility_graph_multiple_cars(myself, other_cars, intersection)



    # load 


Script()










    




