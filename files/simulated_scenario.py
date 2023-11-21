
'''
# this class simulates the advancement in discrete time
'''

from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater

class Simulated_Scenario:
     def __init__(self,cars_array, map, start_time, time_step, num_iterations):
          self.cars = cars_array
          self.map = map
          self.start_time = start_time
          self.time_step = time_step
          self.num_iterations = num_iterations

