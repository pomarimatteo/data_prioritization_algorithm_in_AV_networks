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
        self.cars_in_range = car.cars_in_range
        
        self.obs = []
        
        self.AV = []
        
        #self.show()
        
        #self.fig, self.ax = self.generate_intersection()
    
    
        
    def add_obs(self,obs):
        self.obs.append(obs)
        
    
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
        

        ax.plot(11.09499171133189, 45.60434620845027, 'bo')
        ax.plot(111.095053165378994, 45.60429631978803, 'ro')
        

        
        '''
        # plot myself
        ax.plot(self.car.lat, self.car.long, 'bo')
        
        # plot cars_in_range
        for other_car in self.cars_in_range:
            ax.plot(other_car[0].lat, other_car[0].long, 'ro')
            
        #plot obstacles
        for obs in self.obs:
            ax.plot(obs.lat, obs.long, 'ro')
        '''
        
        return fig, ax
    
    def show(self):
        self.generate_intersection()
        plt.show()
        
        
    def is_point_in_range(self, point):
        x, y = point.x, point.y
        min_x, max_x = self.range[0][0], self.range[1][0]
        min_y, max_y = self.range[0][1], self.range[1][1]

        return min_x <= x <= max_x and min_y <= y <= max_y

    def get_car(self):
        return self.car

    def get_buildings_geometry(self):
        return self.map.buildings['geometry']
    
    def get_buildings(self):
        return self.map.buildings
    
    def get_roads_geometry(self):
        return self.map.roads['geometry']
    
    