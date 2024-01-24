
from AHP_score import AHP_score
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
        
        self.visible_obs = []
        
        self.obstacle_north = []
        self.obstacle_east = []
        self.obstacle_south = []
        self.obstacle_west = []
        
    def get_visible_obs(self):
        return self.visible_obs
    
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
        
    
    
    ########################################################
    # AHP_section
    '''
    a = 9  # ('Novelty', 'Reliability')
    b = 3  # ('Novelty', 'Distance')
    c = 3  # ('Novelty', 'Content')
    d = 1/6  # ('Reliability', 'Distance')
    e = 1/8  # ('Reliability', 'Content')
    f = 1  # ('Distance', 'Content')
    
    matrix = {
        ('Novelty', 'Novelty'): 1,
        ('Novelty', 'Reliability'): a,
        ('Novelty', 'Distance'): b,
        ('Novelty', 'Content'): c,

        ('Reliability', 'Novelty'): 1/a,
        ('Reliability', 'Reliability'): 1,
        ('Reliability', 'Distance'): d,
        ('Reliability', 'Content'): e,

        ('Distance', 'Novelty'): 1/b,
        ('Distance', 'Reliability'): 1/d,
        ('Distance', 'Distance'): 1,
        ('Distance', 'Content'): f,

        ('Content', 'Novelty'): 1/c,
        ('Content', 'Reliability'): 1/e,
        ('Content', 'Distance'): 1/f,
        ('Content', 'Content'): 1,
    }
    
    # conditiona VOI
    values = [
        5, # proximity_relation_strength_value
        5, # n_obstacles_value
        5, #proximity_value
        0.8
    ] #accuracy_value
    '''    



    