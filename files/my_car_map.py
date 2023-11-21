'''
# This class is designed to visualize a map with the car position on it
'''

from map import Map


import matplotlib.pyplot as plt

class My_car_map:

    def __init__(self, car, map):
        self.car = car
        self.map = map
        self.range = map.find_range_plot()
        #self.fig, self.ax = self.generate_intersection()

    
    # private
    def generate_intersection(self):
        fig, ax = plt.subplots()

        # plot streets
        for street in self.map.roads['geometry']:
            x, y = street.coords.xy
            ax.plot(x, y, linewidth=3, color="grey")

        # plot buildings
        for building in self.map.buildings['geometry']:
            ax.plot(*building.exterior.xy, color='green')

        # extract boundaries
        xlim = [self.range[0][0], self.range[0][1]]
        ylim = [self.range[1][0], self.range[1][1]]


        

        plt.xlim(xlim)
        plt.ylim(ylim)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_title("Intersection")
        ax.set_aspect('equal')

        # plot myself
        ax.plot(self.car.lat, self.car.long, 'bo')
        
        return fig, ax
    
    def show(self):
        self.generate_intersection()
        plt.show()

    def get_car(self):
        return self.car
    
    def update_range(self, new_range):
        self.range = self.new_range

    def get_buildings_geometry(self):
        return self.map.buildings['geometry']
    
    def get_buildings(self):
        return self.map.buildings
    
    def get_roads_geometry(self):
        return self.map.roads['geometry']
