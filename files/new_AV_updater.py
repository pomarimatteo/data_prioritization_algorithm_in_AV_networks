'''
# manages when a new AV is detected
'''

import matplotlib.pyplot as plt
from shapely.geometry import Point, LineString


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
        #formatted_distance = float(util.format_distance(dist_in_meters))
        
        return dist_in_meters
    
    def check_in_range(self):
        if (util.check_in_range(self.my_car_map, self.other_car)):
            self.car.cars_in_range.append(self.other_car)

    #check visility static objects
    def check_visibility_SO(self):
        buildings = self.my_car_map.get_buildings()
        my_car_pos = Point(self.car.lat, self.car.long)
        other_car_pos = Point(self.other_car.lat, self.other_car.long)

        return(util_vsb.is_visible(my_car_pos, other_car_pos, buildings ))
        
    def select_camera(self):
        #if not self.check_in_range() or not self.#check_visibility_SO():
        #    return -1
        camera = util_vsb.determine_camera(self.car, self.other_car)
        return camera

    def process_detected_car(self):
        dist = self.calculate_distance()
        tupla = (self.other_car,dist) 
        if(dist < 1000):
            self.car.cars_in_range.append(tupla)
            
            if (self.check_visibility_SO()): 
                camera = self.select_camera()                
                    
                if (camera != -1):   
                    if camera == "North" or camera == "North ":
                        self.car.visible_north.append(tupla)
                    elif camera == "South":
                        self.car.visible_south.append(tupla)
                    elif camera == "East":
                        self.car.visible_east.append(tupla)
                    elif camera == "West":
                        self.car.visible_west.append(tupla)
                    
