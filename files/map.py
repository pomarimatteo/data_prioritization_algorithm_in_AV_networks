'''
# this class takes GeoJSON files and displays a map with streets and buildings 
# ensuring proper visualization using the draw_intersection function.  
'''

import matplotlib.pyplot as plt

class Map:

    def __init__(self, buildings, roads):

        self.buildings = buildings
        self.roads = roads
        self.range = self.find_range_plot()
        
        #self.show()


    # find range for the plot based on buildings coordinates of the geojson file
    def find_range_plot(self):
        min_x, max_x, min_y, max_y = float('inf'), float('-inf'), float('inf'), float('-inf')

        for building in self.buildings['geometry']:
            for point in building.exterior.coords:
                x, y = building.exterior.coords.xy

                min_x = min(min_x, min(x), max(x))
                max_x = max(max_x, min(x), max(x))

                min_y = min(min_y, min(y), max(y))
                max_y = max(max_y, min(y), max(y))

        return([(min_x,max_x),(min_y,max_y)])

    def get_range(self):
        return self.range

    def draw_intersection(self):

        fig, ax = plt.subplots()

        # plot streets
        for street in self.roads['geometry']:
            x, y = street.coords.xy
            ax.plot(x, y, linewidth=15, color="grey")

        # plot buildings
        for building in self.buildings['geometry']:
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

        return fig, ax
        
    def show(self):    
        self.draw_intersection()
        plt.show()

    # new_range must be in the format [(min_x,max_x),(min_y,max_y)]
    def update_range(self, new_range):
        self.range = self.new_range


