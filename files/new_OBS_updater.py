'''
# manages when a new AV is detected
'''
from OBS import Obstacle
import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString
import numpy as np
import random
import math

from utility import Utility as util
from util_visibility import Util_visibility as util_vsb

class New_OBS_updater:
    range_obs = 100 # 50 meters
    

    def __init__(self, my_car_map, obs):
        self.my_car_map = my_car_map
        #my_car_map.show()
        self.obs = obs

        self.car = self.my_car_map.get_car()
        
        
        
        #print(obs.lat,obs.long)
        
        #obs_n = self.add_noise_to_data()
        
        #print(obs_n.lat,obs_n.long)
        #print('******')
        


    # private
    def generate_map(self):
        fig, ax = self.my_car_map.generate_intersection()

        # Plot in-range cars
        ax.plot(self.obs.lat, self.obs.long, 'black')
        
    def show(self):
        self.generate_map()
        plt.show()

    # distance in meters
    def calculate_distance(self):
        coord_p1 = (self.car.lat, self.car.long)
        coord_p2 = (self.obs.lat, self.obs.long)

        dist_in_meters = util.distance_meter(coord_p1, coord_p2)
        #formatted_distance = float(util.format_distance(dist_in_meters))  

        return dist_in_meters
    
    def calculate_priority(self, sender_car, receiver_car, obs):
        #return New_OBS_updater.calculate_distance()
        #Conditional_VOI = CV()
        #Conditional_VOIcalculate_importance_value(self, values):
        
        
        
        return 1
    
    def check_in_range(self):
        if (util.check_in_range(self.my_car_map, self.obs)):
            self.car.cars_in_range.append(self.obs)

    #check visility static objects
    def check_visibility_SO(self):
        buildings = self.my_car_map.get_buildings()
        my_car_pos = Point(self.car.lat, self.car.long)
        obs_pos = Point(self.obs.lat, self.obs.long)

        return(util_vsb.is_visible(my_car_pos, obs_pos, buildings ))
        
    def select_camera(self):
        #if not self.check_in_range() or not self.#check_visibility_SO():
        #    return -1
        camera = util_vsb.determine_camera(self.car, self.obs)
        return camera
                    
    def process_detected_obj(self):
        if (self.check_visibility_SO()): 
            camera = self.select_camera()
            # distance
            dist = self.calculate_distance()    
            if(dist < New_OBS_updater.range_obs):
                tupla = (self.obs,dist)
                self.car.visible_obs.append(tupla)

                if (camera != -1):   
                    if camera == "North" or camera == "North ":
                        self.car.obstacle_north.append(tupla)
                    elif camera == "South":
                        self.car.obstacle_south.append(tupla)
                    elif camera == "East":
                        self.car.obstacle_east.append(tupla)
                    elif camera == "West":
                        self.car.obstacle_west.append(tupla)

    def add_gaussian_noise(self, mean=0, std_dev=0.001):
        # Genera del rumore gaussiano per la latitudine e la longitudine
        lat_noise = np.random.normal(mean, std_dev)
        long_noise = np.random.normal(mean, std_dev)
        
        # Aggiunge il rumore ai valori esistenti
        self.lat += lat_noise
        self.long += long_noise
        
    def plot_gaussian_distribution(mean=0, std_dev=1, xmin=-5, xmax=5):
        x = np.linspace(xmin, xmax, 1000)
        y = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev) ** 2)
        
        plt.plot(x, y, label='Gaussian Distribution')
        plt.title('Gaussian Distribution')
        plt.xlabel('X')
        plt.ylabel('Probability Density')
        plt.legend()
        plt.grid(True)
        plt.show()
       
       
       
       
    def move_point(self, angle, distance):
        
        coord = self.my_car_map.car.lat, self.my_car_map.car.long
        

        # Converti le coordinate da latitudine/longitudine a metri
        lat, lon = coord
        lat_meters_per_degree = 111000
        lon_meters_per_degree = 111000 * np.cos(np.radians(lat))
        
        # Calcola lo spostamento in metri
        delta_lat = np.sin(np.radians(angle)) * distance / lat_meters_per_degree
        delta_lon = np.cos(np.radians(angle)) * distance / lon_meters_per_degree
        
        # Applica lo spostamento alle coordinate
        new_lat = lat + delta_lat
        new_lon = lon + delta_lon
        return new_lat, new_lon

    def add_noise_to_data(self):

        name = self.obs.ID
        lat, lon = self.obs.lat, self.obs.long
            
        noisy_lat, noisy_lon = self.move_point(random.randint(0, 360), 0.1e-12)
            
        noisy_obs = Obstacle(name, noisy_lat, noisy_lon)
        
        return noisy_obs  
       
       
       
    ''' 
    #plot_gaussian_distribution()
    
    obst=Obstacle('obs01', 11.007994965432141, 45.43956251307974)
    
    print("Coordinate iniziali:", obst.lat, obst.long)
    
    # Aggiunta di rumore gaussiano alle coordinate
    add_gaussian_noise(lat_std_dev=0.001, long_std_dev=0.001)
    print("Coordinate con rumore gaussiano:", obst.lat, obst.long)
    '''