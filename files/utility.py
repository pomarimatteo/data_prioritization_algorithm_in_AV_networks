
from geopy.distance import geodesic
#from my_car_map import my_car_map
import math

class Utility:
    @staticmethod
    def distance_meter(point_1, point_2):       
        distance_in_meters = geodesic(point_1, point_2).meters
        truncated_distance = round(distance_in_meters, 2)
        return truncated_distance
    
    def dist_car_obs(car,obs):
        point_1 = (car.lat,car.long)
        point_2 = (obs.lat,obs.long)
        
        return Utility.distance_meter(point_1, point_2)

    def format_distance(dist):
        if dist > 1000:
            dist_in_kilometers = dist / 1000
            formatted_distance = f"{dist_in_kilometers:.2f} km"
        else:
            formatted_distance = f"{dist:.2f} m"
        
        return formatted_distance
    
    def check_in_range(car_map, car_2):
        car_1 = car_map.car
        if car_1 is not car_2:
            diff_lat = abs(car_1.lat - car_2.lat)
            diff_long = abs(car_1.long - car_2.long)

            # Check if the other car is within the specified range and calculate distance
            range = car_map.range

            min_x, max_x = range[0]
            min_y, max_y = range[1]

            # Calcola x_range e y_range
            x_range = max_x - min_x
            y_range = max_y - min_y

            
            return diff_lat <= x_range and diff_long <= y_range
        
        return False

    def calculate_angle(car_1, car_2):
        # Calculate the angle between the camera's direction (point1) and point2
        print(car_2)
        dx = car_2.lat - car_1.lat
        dy = car_2.long - car_1.long
        angle = math.atan2(dy, dx) * 180 / math.pi
        return angle
    
    def calculate_angle(car, obs):
        obstacle_lat = car.lat
        obstacle_long = car.long
        
        # Calcola la differenza tra le coordinate dell'ostacolo e della macchina
        delta_lat = obstacle_lat - self.lat
        delta_long = obstacle_long - self.long
        
        # Calcola l'angolo tra l'orientamento della macchina e la posizione dell'ostacolo
        angle_radians = math.atan2(delta_long, delta_lat)
        angle_degrees = math.degrees(angle_radians)
        
        # Normalizza l'angolo tra 0 e 360 gradi
        angle_from_north = (angle_degrees + 360) % 360
        
        # Calcola l'angolo relativo tra l'orientamento della macchina e l'ostacolo
        relative_angle = angle_from_north - self.orientation
        
        # Normalizza l'angolo relativo tra -180 e 180 gradi
        relative_angle = (relative_angle + 180) % 360 - 180
        
        return relative_angle

    def calculate_angle_opt(car, obs):
        car_lat = car.lat
        car_long = car.long
        car_orientation = car.orientation
        
        obstacle_lat = obs.lat
        obstacle_long = obs.long
        
        
        # Calcola la differenza tra le coordinate dell'ostacolo e della macchina
        delta_lat = obstacle_lat - car_lat
        delta_long = obstacle_long - car_long
        
        # Calcola l'angolo tra l'orientamento della macchina e la posizione dell'ostacolo
        angle_radians = math.atan2(delta_long, delta_lat)
        angle_degrees = math.degrees(angle_radians)
        
        # Normalizza l'angolo tra 0 e 360 gradi
        angle_from_north = (angle_degrees + 360) % 360
        
        # Calcola l'angolo relativo tra l'orientamento della macchina e l'ostacolo
        relative_angle = angle_from_north - car_orientation
        
        # Normalizza l'angolo relativo tra -180 e 180 gradi
        relative_angle = (relative_angle + 180) % 360 - 180
        
        return relative_angle


