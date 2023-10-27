'''
# manages when a new AV is detected
'''

import matplotlib.pyplot as plt

from utility import Utility as util
from util_visibility import Util_visibility as util_vsb

class New_AV_updater:

    def __init__(self, my_car_map, other_car):
        self.my_car_map = my_car_map
        self.other_car = other_car
        self.car = self.my_car_map.get_car()

    # private
    def generate_map(self):
        fig, ax = self.my_car_map.generate_intersection()
        # Plot in-range cars
        ax.plot(self.other_car.lat, self.other_car.long, 'ro')
        
    def show(self):
        self.generate_map()
        plt.show()

    # distance in meters
    def calculate_distance(self):
        coord_p1 = (self.car.lat, self.car.long)
        coord_p2 = (self.other_car.lat, self.other_car.long)

        dist_in_meters = util.distance_meter(coord_p1, coord_p2)
        formatted_distance = util.format_distance(dist_in_meters)
        
        return formatted_distance
    
    def check_in_range(self):
        if (util.check_in_range(self.my_car_map, self.other_car)):
            self.car.cars_in_range.append(self.other_car)

    #check visility static objects
    def check_visibility_SO(self):
        buildings = self.my_car_map.get_buildings_geometry()
        util_vsb.visibility_graph_other_car(self.car, self.other_car, buildings )

        return
    
    def get_camera(self):
        #if (self.check_in_range):
        camera = util_vsb.determine_camera(self.car, self.other_car)
        return camera
        
    def final_camera(self):
        #if not self.check_in_range() or not self.#check_visibility_SO():
        #    return -1

        return(self.get_camera())
    
    def add_car_camera_list(self):
        camera = self.final_camera()
        if (camera != -1):
            self.car.cars_in_range.append(self.other_car)
            
            if camera == "North" or camera == "North ":
                self.car.visible_north.append(self.other_car)
            elif camera == "South":
                self.car.visible_south.append(self.other_car)
            elif camera == "East":
                self.car.visible_east.append(self.other_car)
            elif camera == "West":
                self.car.visible_west.append(self.other_car)

            
    

