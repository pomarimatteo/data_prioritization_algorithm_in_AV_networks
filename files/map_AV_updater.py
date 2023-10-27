'''
# This class visualize a map with the car position and all the other cars in an 
# array
'''

import matplotlib.pyplot as plt


class Map_AV_updater:

    def __init__(self, my_car_map, other_car_array):
        self.my_car_map = my_car_map
        self.other_car_array = other_car_array

    def add_cars(self):
        fig, ax = self.my_car_map.generate_intersection()
        
        # Plot in-range cars
        for other_car in self.other_car_array:
            ax.plot(other_car.lat, other_car.long, 'ro')

    def show(self):
        self.add_cars()
        plt.show()
