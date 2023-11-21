import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import numpy as np
import math

from car import Car

class Util_visibility():

    # if 2 car are visible to each other
    def is_visible(point1, point2, buildings):
        line = LineString([point1, point2])

        for building in buildings['geometry']:
            if line.intersects(building):
                return False
        return True
    
    @staticmethod
    def get_angle(point1, point2):
        delta_x = point2.x - point1.x
        delta_y = point2.y - point1.y
        angle_rad = np.arctan2(delta_y, delta_x)
        angle_deg = np.degrees(angle_rad)
        return angle_deg
    
    # generates the plot and return bool for visibility.
    # init orientation is considerated

    @staticmethod
    def visibility_graph_other_car(my_car, other_car, buildings):
        # Posizione del tuo veicolo
        my_car_pos = Point(my_car.lat, my_car.long)

        # Posizione dell'altro veicolo
        other_car_pos = Point(other_car.lat, other_car.long)

        # Verifica se i punti sono visibili
        visible = Util_visibility.is_visible(my_car_pos, other_car_pos, buildings)

        # Calcola le coordinate dei punti finali delle rette in base all'orientazione iniziale
        angles = [my_car.orientation + angle for angle in range(45, 360, 90)]
        length = 0.0002  # Lunghezza delle rette (sostituire con il valore desiderato)

        x1 = [my_car_pos.x + length * np.cos(np.radians(angle)) for angle in angles]
        y1 = [my_car_pos.y + length * np.sin(np.radians(angle)) for angle in angles]

        # Visualizzazione degli edifici
        buildings.plot(edgecolor='k', facecolor='none', alpha=0.7, figsize=(10, 10))

        # Visualizzazione dei punti dei veicoli
        plt.scatter(*my_car_pos.coords.xy, color='red', label='My Car', s=50, zorder=2)
        plt.scatter(*other_car_pos.coords.xy, color='blue', label='Other Car', s=50, zorder=2)

        # Visualizzazione della LineString tra i punti
        line = LineString([my_car_pos, other_car_pos])  # Aggiunta della definizione della LineString
        x, y = line.xy
        plt.plot(x, y, color='green', linestyle='--', label='LineString', zorder=1)

        # Visualizzazione delle rette
        for i, angle in enumerate(angles):
            plt.plot([my_car_pos.x, x1[i]], [my_car_pos.y, y1[i]], label=f'{angle} degrees', linestyle='--', zorder=1, color='navy')

        plt.legend()
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Visualizzazione Punti, Edifici, LineString e Rette')
        plt.axis('equal')
        #plt.show()

    
    @staticmethod
    def show_visibility_graph_other_car(my_car, other_car, buildings):
        Util_visibility.visibility_graph_other_car(my_car, other_car, buildings)
        plt.show()

    @staticmethod
    def calculate_angle(x1, y1, x2, y2):
            delta_x = x2 - x1
            delta_y = y2 - y1
            angle = math.degrees(math.atan2(delta_y, delta_x))
            return angle if angle >= 0 else angle + 360
    
    def determine_camera(my_car, other_car):
        orientation = my_car.orientation

        # Calculate the angle between the first car (point_1) and the second car (point_2)
        angle = Util_visibility.calculate_angle(my_car.lat, my_car.long, other_car.lat, other_car.long)

        
        # Consider the orientation of the first car
        adjusted_angle = (angle - orientation) % 360

        #adjusted_angle = angle

        #print('angle between ',my_car.ID,' and',other_car.ID,' ',adjusted_angle)

        # Find the camera corresponding to the angle


        camera_directions = {
            "North": (0, 45),
            "West": (45, 135),
            "South": (135, 225),
            "East": (225, 315),
            "North ": (315, 360),  
        }
        
        for camera, (start, end) in camera_directions.items():
            if start <= adjusted_angle < end:
                return camera


        return "-1"

    # shows the intersection and the lines that connect all the cars to myself
    # still to considerate initial orientation
    @staticmethod
    def show_visibility_graph_multiple_cars(my_car, other_cars, buildings):
        # Your vehicle's position
        my_car_pos = Point(my_car.lat, my_car.long)

        # Display buildings
        buildings.plot(edgecolor='k', facecolor='none', alpha=0.7, figsize=(10, 10))

        # Display your vehicle's point
        plt.scatter(*my_car_pos.coords.xy, color='red', label='My Car', s=50, zorder=2)

        # Calculate coordinates of line endpoints
        angles = list(range(45, 360, 90))
        length = 0.0002  # Length of the lines (replace with desired value)

        x1 = [my_car_pos.x + length * np.cos(np.radians(angle)) for angle in angles]
        y1 = [my_car_pos.y + length * np.sin(np.radians(angle)) for angle in angles]
        
        for i, angle in enumerate(angles):
            plt.plot([my_car_pos.x, x1[i]], [my_car_pos.y, y1[i]], linestyle='-', zorder=1, color='black', alpha=0.5)  # Adjust the alpha value as needed

        for other_car in other_cars:
            # Other vehicle's position
            other_car_pos = Point(other_car.lat, other_car.long)

            # Display the other vehicle's point
            plt.scatter(*other_car_pos.coords.xy, s=50, zorder=2)

            # Display the LineString between the points
            line = LineString([my_car_pos, other_car_pos])  # Adding LineString definition
            x, y = line.xy
            plt.plot(x, y, linestyle='--', zorder=1)

        # Graph configuration
        #plt.legend()
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Intersection')
        plt.axis('equal')

        # Show the graph
        plt.show()


