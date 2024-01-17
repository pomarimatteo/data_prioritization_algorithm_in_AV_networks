from utility import Utility as util
from shapely.geometry import Point, LineString
from util_visibility import Util_visibility as util_vsb
from geopy.distance import geodesic
import matplotlib.pyplot as plt

from shapely.geometry import Point
from OBS import Obstacle  # Assuming you have an Obstacle class defined
import geopandas as gpd



class OBS_in_map:
    def __init__(self, my_car_map, obs):
         self.my_car_map = my_car_map
         self.obs = obs

    def manage_obs(self):
        # add obs in 'obs' array in 'my_car_map'
        self.my_car_map.obs.append(self.obs)
        
        dist = self.calculate_my_dist()
     
    def calculate_my_dist(self):
        my_lat = self.my_car_map.get_car().lat
        my_long = self.my_car_map.get_car().long
        obs_lat = self.obs.lat
        obs_long = self.obs.long
        
        return (util.distance_meter((my_lat, my_long),(obs_lat, obs_long)))

            
    def obs_in_LoS(self):
        # Get the coordinates of the car
        myself = Point(self.my_car_map.get_car().lat, self.my_car_map.get_car().long)

        # Iterate over each Obstacle object in the list
        for obstacle in self.obs:
            # Get the coordinates of the obstacle
            obs_point = Point(obstacle.lat, obstacle.long)

            # Check if the obstacle is visible from the car
            if util_vsb.is_visible(myself, obs_point, self.my_car_map.get_buildings()):
                # If visible, append the obstacle to the list of visible obstacles for the car
                self.my_car_map.get_car().visible_obs.append(obstacle)

            
            
    def distance_other_car(self, other_car):
        lat = self.other_car.lat
        long = self.other_car.long
        obs_lat = self.obs.lat
        obs_long = self.obs.long
        
        return (util.distance_meter((lat, long),(obs_lat, obs_long)))
    
    def LoS_other_car(self,other_car):
        other_car = Point(self.other_car.lat,other_car.long)
        obs_point = Point(self.obs.lat, self.obs.long)
        if (util_vsb.is_visible(other_car,obs_point,self.my_car_map.get_buildings())):
            other_car.visible_obs.append(self.obs)
        
    def distance_cars_in_range(self):
        distances = []

        for car in self.my_car_map.cars_in_range:
            car_point = Point(car.lat, car.long)
            dist = util.distance_meter((self.obs.lat, self.obs.long), (car.lat, car.long))
            distances.append((car, dist))

        return distances
            
    def LoS_with_cars_in_range(self):
        myself = Point(self.my_car_map.get_car.lat, self.my_car_map.get_car.long)
        obs_point = Point(self.obs.lat, self.obs.long)
        cars_with_los = []

        for car in self.my_car_map.cars_in_range:
            car_point = Point(car.lat, car.long)
            if util_vsb.is_visible(obs_point, car_point,self.my_car_map.get_buildings()):
                cars_with_los.append(car)

        return cars_with_los
    
    def print_distance_cars_in_range(self):
        distances_to_cars = self.distance_cars_in_range()
        for car, dist in distances_to_cars:
            print(f"Distance from obs to car {car.ID}: {dist} meters")
    
    def print_cars_with_los(self):
        # Get the coordinates of the car
        myself = Point(self.my_car_map.get_car().lat, self.my_car_map.get_car().long)

        # Iterate over each Obstacle object in the list
        for obstacle in self.obs:
            # Get the coordinates of the obstacle
            obs_point = Point(obstacle.lat, obstacle.long)

            # Print information for the current obstacle
            print(f"Line of Sight Information for Obstacle {obstacle.ID}:")
            print("-" * 30)

            # Iterate over each car in range
            for car in self.my_car_map.cars_in_range:
                # Get the coordinates of the car
                car_point = Point(car.lat, car.long)

                # Check if the car has line of sight with the obstacle
                if util_vsb.is_visible(obs_point, car_point, self.my_car_map.get_buildings()):
                    print(f"Car {car.ID} has Line of Sight with the obstacle.")

            print("-" * 30)

        
    def plot(self):
        fig, ax = self.my_car_map.generate_intersection()
        #objs = self.generate_random_obstacles()

        for obs in self.obs:
            ax.plot(obs.lat, obs.long, marker='^', color='black', markersize=5)

        
        plt.show()
        
        
    
    '''
    def plot_map(self):
        # Estrai i dati geospaziali dalla mappa e dagli ostacoli
       
        map_geometry = self.my_car_map.get_roads_geometry()
        
        obs_geometry = gpd.GeoDataFrame(geometry=[Point(obs.lat, obs.long) for obs in self.my_car_map.obs])

        # Crea un GeoDataFrame con gli ostacoli e la mappa
        obstacles_gdf = gpd.GeoDataFrame(geometry=obs_geometry.geometry)
        map_gdf = gpd.GeoDataFrame(geometry=map_geometry)

        # Plotta la mappa
        fig, ax = plt.subplots(figsize=(10, 10))
        map_gdf.plot(ax=ax, color='lightgray', edgecolor='black', alpha=0.5)

        # Plotta gli ostacoli
        obstacles_gdf.plot(ax=ax, color='red', marker='o', markersize=50)

        # Plotta la posizione del veicolo
        vehicle_point = Point(self.my_car_map.car.lat, self.my_car_map.car.long)
        gpd.GeoDataFrame(geometry=[vehicle_point]).plot(ax=ax, color='blue', marker='^', markersize=100)

        plt.title("Mappa con Ostacoli e Posizione del Veicolo")
        plt.xlabel("Longitudine")
        plt.ylabel("Latitudine")
        plt.show()
        '''
        