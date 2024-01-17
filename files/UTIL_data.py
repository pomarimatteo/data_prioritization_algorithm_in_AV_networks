import random
from shapely.geometry import Point
from OBS import Obstacle

class Data:

    @staticmethod
    def generate_random_obstacles(my_car_map, num_obstacles):
        # Extract building polygons from the map

        #building_polygons = my_car_map.map.geometry
        building_polygons = my_car_map.get_buildings_geometry()

        # List to store generated obstacles
        obstacles = []

        # Define the bounding box of the map
        map_bounds = my_car_map.range
        print('map bounds: ',map_bounds[0][0], map_bounds[0][1])
        print('map bounds: ',map_bounds[1][0], map_bounds[1][1])

        #map_bounds = my_car_map.map.total_bounds

        # Generate random obstacles
        for _ in range(num_obstacles):
            # Randomly generate a point within the map bounds
            random_point = None
            while random_point is None or not my_car_map.is_point_in_range(random_point):
                random_point = Point(random.uniform(map_bounds[0][0], map_bounds[0][1]),
                                    random.uniform(map_bounds[1][0], map_bounds[1][1]))

            # Check if the point is outside building polygons
            inside_building = any(random_point.within(building) for building in building_polygons)

            # If the point is inside a building, generate a new one
            
            while inside_building:
                random_point = None
                while random_point is None or not my_car_map.is_point_in_range(random_point):
                    random_point = Point(random.uniform(map_bounds[0][0], map_bounds[0][1]),
                                        random.uniform(map_bounds[1][0], map_bounds[1][1]))
                inside_building = any(random_point.within(building) for building in building_polygons)
            

            # Create an obstacle using the generated point
            obstacle = Obstacle(ID=_ + 1, lat=random_point.x, long=random_point.y)
            print('_')
            print(random_point.x, random_point.y)
            # Append the obstacle to the list
            obstacles.append(obstacle)


        return obstacles