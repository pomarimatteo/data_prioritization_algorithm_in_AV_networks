from utility import Utility as util
from shapely.geometry import Point, LineString
from util_visibility import Util_visibility as util_vsb
from geopy.distance import geodesic



class OBS_in_map:
    def __init__(self, my_car_map, obs):
         self.my_car_map = my_car_map
         self.obs = obs

    def manage_obs(self):
        # add obs in 'obs' array in 'my_car_map'
        self.my_car_map.obs.append(self.obs)
        
        dist = self.calculate_my_dist()
     
    def calculate_my_dist(self):
        my_lat = self.my_car_map.get_car().lat
        my_long = self.my_car_map.get_car().long
        obs_lat = self.obs.lat
        obs_long = self.obs.long
        
        return (util.distance_meter((my_lat, my_long),(obs_lat, obs_long)))

    def obs_in_LoS(self):
        myself = Point(self.my_car_map.get_car().lat,self.my_car_map.get_car().long)
        obs_point = Point(self.obs.lat, self.obs.long)
        if (util_vsb.is_visible(myself,obs_point,self.my_car_map.get_buildings())):
            self.my_car_map.get_car().visible_obs.append(self.obs)
            
            
    def distance_other_car(self, other_car):
        lat = self.other_car.lat
        long = self.other_car.long
        obs_lat = self.obs.lat
        obs_long = self.obs.long
        
        return (util.distance_meter((lat, long),(obs_lat, obs_long)))
    
    def LoS_other_car(self,other_car):
        other_car = Point(self.other_car.lat,other_car.long)
        obs_point = Point(self.obs.lat, self.obs.long)
        if (util_vsb.is_visible(other_car,obs_point,self.my_car_map.get_buildings())):
            other_car.visible_obs.append(self.obs)
        
        
    def distance_cars_in_range(self):
        distances = []

        for car in self.my_car_map.cars_in_range:
            car_point = Point(car.lat, car.long)
            dist = util.distance_meter((self.obs.lat, self.obs.long), (car.lat, car.long))
            distances.append((car, dist))

        return distances
            
    def LoS_with_cars_in_range(self):
        myself = Point(self.my_car_map.get_car.lat, self.my_car_map.get_car.long)
        obs_point = Point(self.obs.lat, self.obs.long)
        cars_with_los = []

        for car in self.my_car_map.cars_in_range:
            car_point = Point(car.lat, car.long)
            if util_vsb.is_visible(obs_point, car_point,self.my_car_map.get_buildings()):
                cars_with_los.append(car)

        return cars_with_los
    
    
    def print_distance_cars_in_range(self):
        distances_to_cars = self.distance_cars_in_range()
        for car, dist in distances_to_cars:
            print(f"Distance from obs to car {car.ID}: {dist} meters")
    
    def print_cars_with_los(self):
        myself = Point(self.my_car_map.get_car().lat, self.my_car_map.get_car().long)
        obs_point = Point(self.obs.lat, self.obs.long)
        
        print(f"Line of Sight Information for Obstacle {self.obs.ID}:")
        print("-" * 30)

        for car in self.my_car_map.cars_in_range:
            car_point = Point(car.lat, car.long)
            if util_vsb.is_visible(obs_point, car_point,self.my_car_map.get_buildings()):
                print(f"Car {car.ID} has Line of Sight with the obstacle.")
        
        print("-" * 30)