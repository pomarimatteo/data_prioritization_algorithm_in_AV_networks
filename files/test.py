from map import Map
from car import Car
from my_car_map import my_car_map

from utility import Utility as util
from util_visibility import Util_visibility as util_vsb

import geopandas as gpd 


# import geojson files
intersection = gpd.read_file('data/intersection.geojson')

single_building = gpd.read_file('data/single_building.geojson')

road = gpd.read_file('data/road.geojson')

# containers 
maps = [] 
cars = []
my_car_map_array = []

map_data = [(intersection, road),
            (single_building, road)]

for buildings, roads in map_data:
    maps.append(Map(buildings, roads))



'''
# Create cars and add them to the list
car_data = [
    ('A', 11.007767285707814, 45.439492436628484, math.pi/2),
    ('B', 11.007789421555742, 45.43937903284822, math.pi/2),
    ('C', 11.007903263242582, 45.439586043947855, math.pi),
    ('D', 11.007484262837124, 45.43954676351245, 0),
    ('E', 11.008225211533869, 45.43960992760452, math.pi),
    ('F', 11.007983298078727, 45.439737059970014, math.pi*3/2)
]
'''

# Create cars and add them to the list
car_data = [
    ('A', 11.007767285707814, 45.439492436628484, 45),
    ('B', 11.007789421555742, 45.43937903284822, 90),
    ('C', 11.007903263242582, 45.439586043947855, 90),
    ('D', 11.007484262837124, 45.43954676351245, 90),
    ('E', 11.008225211533869, 45.43960992760452, 90),
    ('F', 11.007983298078727, 45.439737059970014, 90)]


for ID, x, y, orientation in car_data:
    cars.append(Car(ID, x, y, orientation))


# generate map of the surroundings for each AV

for car in cars:
    my_car_map_array.append(my_car_map(car,maps[0]))



'''
for car in cars:
    util_vsb.show_visibility_graph_other_car(cars[0], car, intersection)
'''


print(util_vsb.determine_camera(cars[0],cars[1],cars[0].orientation))
#print(util_vsb.determine_camera(cars[0],cars[2],cars[0].orientation))
#print(util_vsb.determine_camera(cars[0],cars[3],cars[0].orientation))
#print(util_vsb.determine_camera(cars[0],cars[4],cars[0].orientation))
#print(util_vsb.determine_camera(cars[0],cars[5],cars[0].orientation))


util_vsb.show_visibility_graph_multiple_cars(cars[0], cars, intersection)

#util_vsb.visibility_graph_other_car(cars[0],[cars[1],cars[2],cars[3],cars[4],cars[5]],intersection)



#util_vsb.visualize_visibility(my_car_map_array[0],[cars[2]])

