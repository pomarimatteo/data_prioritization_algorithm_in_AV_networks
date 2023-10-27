'''
# This class represents a vehicle with its attributes 
'''

class Car:
    def __init__(self, ID, lat, long, orientation):

        self.ID = ID
        self.lat = lat
        self.long = long
        self.orientation = orientation

        self.cars_in_range = []

        self.visible_north = []
        self.visible_east = []
        self.visible_south = []
        self.visible_west = []
        
    def get_cars_in_range(self):
        return self.cars_in_range
    
    def get_visible_north(self):
        return self.visible_north

    def get_visible_east(self):
        return self.visible_east

    def get_visible_south(self):
        return self.visible_south

    def get_visible_west(self):
        return self.visible_west

    def print_car_info(self):
        car_ids = [car.ID for car in self.cars_in_range]
        north_ids = [car.ID for car in self.visible_north]
        east_ids = [car.ID for car in self.visible_east]
        south_ids = [car.ID for car in self.visible_south]
        west_ids = [car.ID for car in self.visible_west]

        print(f"CAR {self.ID}")
        print("cars_in_range:", ", ".join(car_ids))
        print("north:", ", ".join(north_ids))
        print("east:", ", ".join(east_ids))
        print("south:", ", ".join(south_ids))
        print("west:", ", ".join(west_ids))

    
    
    
    



    