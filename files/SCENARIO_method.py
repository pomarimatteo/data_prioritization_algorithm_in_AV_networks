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

class Simulated_Scenario:
     
     # **************************************************** #
     
     # 1) generate n random AVs
     
     # 2) generate m random obstacles
     
     # 3) verify each obstacle in every LoS
     
     # 4) evaluate the broadcast communication
     
     # 5) implement consideration and AHP for prioritarization of the data
     
     # 6) evaluate the new communication
     
     # **************************************************** #
               
     # Define file paths as variables
     geojson_path = 'data/geojson/'
     
     # Import geojson files
     intersection = gpd.read_file(geojson_path + 'map_001.geojson')
     road = gpd.read_file(geojson_path + 'road.geojson')
     
     # Generate map
     map = Map(intersection, road)
     
     #def __init__(self):
     #     array_AVs = self.generate_all_AVs()
     
     # **************************************************** #

     # SCENARIO_run_overview
     def generate_all_AVs():
          array_AVs = []
          car_data = [
               ('A', 11.007767285707814, 45.439492436628484, 90),
               ('B', 11.007789421555742, 45.43937903284822, 90),
               ('C', 11.007903263242582, 45.439586043947855, 180),
               ('D', 11.007484262837124, 45.43954676351245, 0),
               ('E', 11.008225211533869, 45.43960992760452, 180),
               ('F', 11.007983298078727, 45.439737059970014, 270)]
               
          for ID, x, y, orientation in car_data:
               array_AVs.append(Car(ID, x, y, orientation))
                    
          return array_AVs
          
     def generate_all_car_map(array_AVs):
          
          array_car_map = []
          for car in array_AVs:
               array_car_map.append(My_car_map(car,Simulated_Scenario.map))
               
          return array_car_map
          
     def process_all_AVs(array_car_map):
          for AV in array_car_map:
               array_without_AV = [item.car for item in array_car_map if item != AV]

               Simulated_Scenario.detect_other_AVs(AV, array_without_AV)
          
     def generate_spawn_zone():
          polygon_coords = [
          [11.0069841, 45.4395318],
          [11.0069716, 45.4394266],
          [11.0077328, 45.4395250],
          [11.0077888, 45.4393060],
          [11.0078187, 45.4393031],
          [11.0077820, 45.4395357],
          [11.0086243, 45.4395781],
          [11.0085992, 45.4396572]]
          
          return Polygon(polygon_coords), polygon_coords
          
     def generate_obstacles(n_obs):
          polygon, polygon_coords = Simulated_Scenario.generate_spawn_zone()
          obstacle_data = []
          for i in range(n_obs):
               # Generating a random point inside the polygon
               while True:
                    x = random.uniform(min(p[0] for p in polygon_coords), max(p[0] for p in polygon_coords))
                    y = random.uniform(min(p[1] for p in polygon_coords), max(p[1] for p in polygon_coords))
                    point = Point(x, y)
                    
                    # Checking if the point is inside the polygon
                    if polygon.contains(point):
                         break

               # Adding the obstacle to the list
               obstacle_data.append(('obs{:02d}'.format(i + 1), x, y))
          
          obs_array = []
          
          for data in obstacle_data:
               obs = Obstacle(data[0], data[1], data[2])
               obs_array.append(obs)
               
          return obs_array

     def process_obs(obs_array):
          
          
          return
     
     def info_AV(array_AVs):
          for car in array_AVs:
               car.print()
          
          
     # SCENARIO_run
     def generate_myself():
          my_latitude = 11.007767285707814
          my_longitude = 45.439492436628484
          my_orientation = 90
          
          myself = Car('A', my_latitude, my_longitude, my_orientation)

          # Generate my_car_map
          my_car_map = My_car_map(myself,Simulated_Scenario.map)
          return my_car_map
          
     def generate_AVs():
          other_cars = []
          car_data = [
               ('B', 11.007789421555742, 45.43937903284822, 90),
               ('C', 11.007903263242582, 45.439586043947855, 90),
               ('D', 11.007484262837124, 45.43954676351245, 90),
               ('E', 11.008225211533869, 45.43960992760452, 90),
               ('F', 11.007983298078727, 45.439737059970014, 90)]
               
          for ID, x, y, orientation in car_data:
               other_cars.append(Car(ID, x, y, orientation))
                    
          return other_cars
     
     def detect_other_AVs(my_car_map, other_AVs):
          for other_AV in other_AVs:
               event = New_AV_updater(my_car_map, other_AV)
               event.process_detected_car()
     
     

          
     
     #my_car_map.show()
     
     
     # OBSTACLES MANAGEMENT
     # n_obs = 5
     # obs_array = Data.generate_random_obstacles(my_car_map, n_obs)

     '''
     obs_event = OBS_in_map(my_car_map,obs_array)
     print(obs_event.obs_in_LoS())
     
     obs_event.plot()
     
     for obs in obs_array:
          New_AV_updater(my_car_map, obs).process_detected_obj()
     myself.print_obstacle_ids()
     
     '''
          
     #def generate_obs():
          