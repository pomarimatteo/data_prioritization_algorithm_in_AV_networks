'''
# manages when a new AV is detected
'''

import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString


from utility import Utility as util
from util_visibility import Util_visibility as util_vsb

class New_OBS_updater:
    range_obs = 100 # 100 meters
    

    def __init__(self, my_car_map, obs):
        self.my_car_map = my_car_map
        self.obs = obs
        self.car = self.my_car_map.get_car()

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
    
    def calculate_priority(self):
        #return New_OBS_updater.calculate_distance()
        #Conditional_VOI = CV()
        #Conditional_VOIcalculate_importance_value(self, values):
        
        return
    
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

