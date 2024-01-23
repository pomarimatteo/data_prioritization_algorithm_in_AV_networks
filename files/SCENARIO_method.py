from map import Map
from car import Car
from my_car_map import My_car_map
from map_AV_updater import Map_AV_updater
from new_AV_updater import New_AV_updater
from OBS import Obstacle
from OBS_in_map import OBS_in_map
from UTIL_data import Data
from new_OBS_updater import New_OBS_updater
import pandas as pd
import numpy as np
import seaborn as sns
from AHP import AHP
from AHP_conditional_VOI import Conditional_VOI



from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from utility import Utility as util
from util_visibility import Util_visibility as util_vsb
from shapely.geometry import Point
import json
import random
import matplotlib.pyplot as plt


import geopandas as gpd 

class Simulated_Scenario:
                    
     # Define file paths as variables
     geojson_path = 'data/geojson/'
     
     # Import geojson files
     intersection = gpd.read_file(geojson_path + 'map_001.geojson')
     road = gpd.read_file(geojson_path + 'road.geojson')
     
     n_obs = 10
     
     # Generate map
     map = Map(intersection, road)
          
     def __init__(self):
          self.array_AVs = self.generate_all_AVs()
          self.array_car_map = self.generate_all_car_map(self.array_AVs)
          self.obs_array = self.generate_obstacles(Simulated_Scenario.n_obs)
          self.obstacles_visibility_info = {}
          
          # param of scenario
          '''
          self.polygon_spawn
          self.car_data
          self.n_obs
          self.intersection
          self.road
          '''
     # **************************************************** #

     # SCENARIO_run_overview
     def generate_all_AVs(self):
          array_AVs = []
          car_data = [
               ('A', 11.007767285707814, 45.439492436628484, 90),
               ('B', 11.007789421555742, 45.43937903284822, 90),
               ('C', 11.007903263242582, 45.439586043947855, 180),
               ('D', 11.007484262837124, 45.43954676351245, 0),
               ('E', 11.008225211533869, 45.43960992760452, 180),
               ('F', 11.007983298078727, 45.439737059970014, 270)]
               
          for ID, x, y, orientation in car_data:
               array_AVs.append(Car(ID, x, y, orientation))
                    
          return array_AVs
          
     def generate_all_car_map(self,array_AVs):
          
          array_car_map = []
          for car in array_AVs:
               array_car_map.append(My_car_map(car,self.map))
               
          return array_car_map
          
     def process_all_AVs(self):
          for AV_map in self.array_car_map:
               array_without_AV_map = [item.car for item in self.array_car_map if item != AV_map]

               self.detect_other_AVs(AV_map, array_without_AV_map)
      
     # private         
     def detect_other_AVs(self, my_car_map, other_AVs):
          for other_AV in other_AVs:
               event = New_AV_updater(my_car_map, other_AV)
               event.process_detected_car()
          
     def generate_spawn_zone(self):
          polygon_coords = [
          [11.0069841, 45.4395318],
          [11.0069716, 45.4394266],
          [11.0077328, 45.4395250],
          [11.0077888, 45.4393060],
          [11.0078187, 45.4393031],
          [11.0077820, 45.4395357],
          [11.0086243, 45.4395781],
          [11.0085992, 45.4396572]]
          
          return Polygon(polygon_coords), polygon_coords
          
     def generate_obstacles(self, n_obs):
          polygon, polygon_coords = self.generate_spawn_zone()
          obstacle_data = []
          for i in range(n_obs):
               # Generating a random point inside the polygon
               while True:
                    x = random.uniform(min(p[0] for p in polygon_coords), max(p[0] for p in polygon_coords))
                    y = random.uniform(min(p[1] for p in polygon_coords), max(p[1] for p in polygon_coords))
                    point = Point(x, y)
                    
                    # Checking if the point is inside the polygon
                    if polygon.contains(point):
                         break

               # Adding the obstacle to the list
               obstacle_data.append(('obs{:02d}'.format(i + 1), x, y))
          
          obs_array = []
          
          for data in obstacle_data:
               obs = Obstacle(data[0], data[1], data[2])
               obs_array.append(obs)
               
          return obs_array

     def process_all_obs(self):
          for AV_map in self.array_car_map:

               self.process_obs(AV_map, self.obs_array)   
          
     #private         
     def process_obs(self, my_car_map, obs_array):
          for other_AV in obs_array:
               event = New_OBS_updater(my_car_map, other_AV)
               event.process_detected_obj()
     
     def info_AV(self):
          for car in self.array_AVs:
               car.print()
          
     def to_json(self):
        data = {
            'AVs': [],
            'Obstacles': [],
            'CarsInRange': [],
            'VisibleObs': [],
            'ObstacleNorth': [],
            'ObstacleEast': [],
            'ObstacleSouth': [],
            'ObstacleWest': [],
            'VisibleNorth': [],
            'VisibleEast': [],
            'VisibleSouth': [],
            'VisibleWest': []
        }

        for car_map in self.array_car_map:
            car_data = {
                'ID': car_map.car.ID,
                'lat': car_map.car.lat,
                'long': car_map.car.long,
                'orientation': car_map.car.orientation,
                'cars_in_range': [car.ID for car in car_map.car.cars_in_range],
                'visible_obs': [obs.ID for obs in car_map.car.visible_obs],
                'obstacle_north': [obs.ID for obs in car_map.car.obstacle_north],
                'obstacle_east': [obs.ID for obs in car_map.car.obstacle_east],
                'obstacle_south': [obs.ID for obs in car_map.car.obstacle_south],
                'obstacle_west': [obs.ID for obs in car_map.car.obstacle_west],
                'visible_north': [obs.ID for obs in car_map.car.visible_north],
                'visible_east': [obs.ID for obs in car_map.car.visible_east],
                'visible_south': [obs.ID for obs in car_map.car.visible_south],
                'visible_west': [obs.ID for obs in car_map.car.visible_west]
            }
            data['AVs'].append(car_data)

        for obs in self.obs_array:
            obs_data = {
                'ID': obs.ID,
                'lat': obs.lat,
                'long': obs.long
            }
            data['Obstacles'].append(obs_data)

        with open('data/scenario_data.json', 'w') as json_file:
            json.dump(data, json_file, indent=4)     
               
     def to_excel(self, excel_path='data/scenario_data.xlsx'):
          data = {
               'ID': [],
               'Latitude': [],
               'Longitude': [],
               'Orientation': [],
               'CarsInRange': [],
               'VisibleObs': [],
               'ObstacleNorth': [],
               'ObstacleEast': [],
               'ObstacleSouth': [],
               'ObstacleWest': [],
               'VisibleNorth': [],
               'VisibleEast': [],
               'VisibleSouth': [],
               'VisibleWest': []
          }

          for car_map in self.array_car_map:
               data['ID'].append(car_map.car.ID)
               data['Latitude'].append(car_map.car.lat)
               data['Longitude'].append(car_map.car.long)
               data['Orientation'].append(car_map.car.orientation)
               
               # Converti le tuple (obs, dist) in formato '(obs.ID, dist)'
               data['CarsInRange'].append(', '.join(f'({car.ID}, {dist})' for car, dist in car_map.car.cars_in_range))

               data['VisibleObs'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.visible_obs))
               data['ObstacleNorth'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.obstacle_north))
               data['ObstacleEast'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.obstacle_east))
               data['ObstacleSouth'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.obstacle_south))
               data['ObstacleWest'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.obstacle_west))
               data['VisibleNorth'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.visible_north))
               data['VisibleEast'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.visible_east))
               data['VisibleSouth'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.visible_south))
               data['VisibleWest'].append(', '.join(f'({obs.ID}, {dist})' for obs, dist in car_map.car.visible_west))

          df = pd.DataFrame(data)
          df.to_excel(excel_path, index=False)
          print(f"Dati esportati correttamente in '{excel_path}'.")

     #potrebbe essere quello ottimale
     def generate_messages_to_send(self):
        messages_to_send = []

        for sender_car_map in self.array_car_map:
            sender_id = sender_car_map.car.ID

            for receiver_car_map in self.array_car_map:
                receiver_id = receiver_car_map.car.ID

                if sender_id != receiver_id:
                    # Gather visible obstacles from sender_car_map
                    visible_obstacles_north = [(obs.ID, dist) for obs, dist in sender_car_map.car.visible_north if obs.ID]
                    visible_obstacles_south = [(obs.ID, dist) for obs, dist in sender_car_map.car.visible_south if obs.ID]
                    visible_obstacles_east = [(obs.ID, dist) for obs, dist in sender_car_map.car.visible_east if obs.ID]
                    visible_obstacles_west = [(obs.ID, dist) for obs, dist in sender_car_map.car.visible_west if obs.ID]

                    # Check if receiver needs information about any obstacles
                    obstacles_to_send = []
                    if any(obstacle for obstacle in visible_obstacles_north if obstacle not in receiver_car_map.car.visible_north):
                        obstacles_to_send.append(("north", visible_obstacles_north))
                    if any(obstacle for obstacle in visible_obstacles_south if obstacle not in receiver_car_map.car.visible_south):
                        obstacles_to_send.append(("south", visible_obstacles_south))
                    if any(obstacle for obstacle in visible_obstacles_east if obstacle not in receiver_car_map.car.visible_east):
                        obstacles_to_send.append(("east", visible_obstacles_east))
                    if any(obstacle for obstacle in visible_obstacles_west if obstacle not in receiver_car_map.car.visible_west):
                        obstacles_to_send.append(("west", visible_obstacles_west))

                    # Generate messages for each direction
                    for direction, obstacles in obstacles_to_send:
                        message = {
                            'sender_id': sender_id,
                            'receiver_id': receiver_id,
                            'direction': direction,
                            'obstacles': obstacles
                        }
                        messages_to_send.append(message)

        return messages_to_send
        
     # broadcast scenario
     def simulate_communication_broadcast(self):
          total_messages_sent = 0
          # Dictionary to keep track of which obstacles are known to each vehicle in each direction
          obstacles_known = {car.ID: {'north': set(), 'south': set(), 'east': set(), 'west': set()} for car in self.array_AVs}

          # Dictionary to count how many messages each vehicle sends
          messages_sent_count = {car.ID: 0 for car in self.array_AVs}

          # Dictionary to count how many messages each vehicle receives
          messages_received_count = {car.ID: 0 for car in self.array_AVs}

          for sender_car_map in self.array_car_map:
               sender_id = sender_car_map.car.ID

               for receiver_car_map in self.array_car_map:
                    receiver_id = receiver_car_map.car.ID

                    if sender_id != receiver_id:
                         # Determine which obstacles the sender should send to the receiver in each direction
                         messages_to_send = self.determine_messages_to_send(sender_car_map, receiver_car_map, obstacles_known)

                         # Update the obstacles known by the receiver
                         obstacles_known[receiver_id] = self.update_obstacles_known(receiver_car_map, messages_to_send, obstacles_known[receiver_id])

                         # Increment the count of messages sent by the sender and received by the receiver
                         messages_sent_count[sender_id] += len(messages_to_send)
                         messages_received_count[receiver_id] += len(messages_to_send)

                         total_messages_sent += len(messages_to_send)

                         # Print information about the sent messages
                         if messages_to_send:
                              print(f"Car {sender_id} sends images to Car {receiver_id}:", messages_to_send)

          # Print the total count of messages sent and received by each vehicle
          for car_id in messages_sent_count.keys():
               print(f"Car {car_id} sends {messages_sent_count[car_id]} messages and receives {messages_received_count[car_id]} messages.")

          print(f"Total messages sent during the simulation: {total_messages_sent}")

          self.plot_message_counts(messages_sent_count, messages_received_count)

     def determine_messages_to_send(self, sender_car_map, receiver_car_map, obstacles_known):
          messages_to_send = []

          for direction in ['north', 'south', 'east', 'west']:
               obstacles_sender = getattr(sender_car_map.car, f'obstacle_{direction}')
               obstacles_receiver_known = obstacles_known.get(receiver_car_map.car.ID, {}).get(direction, set())

               for obs_sender, dist_sender in obstacles_sender:
                    if obs_sender.ID and obs_sender.ID not in obstacles_receiver_known:
                         # Invia il messaggio se l'ostacolo non è noto al receiver in quella direzione
                         messages_to_send.append({'direction': direction, 'obstacle': (obs_sender.ID, dist_sender)})

          return messages_to_send
     
     def update_obstacles_known(self, receiver_car_map, messages_to_send, obstacles_known):
          receiver_id = receiver_car_map.car.ID
          updated_obstacles_known = obstacles_known.get(receiver_id, {}).copy()

          for message in messages_to_send:
               direction = message['direction']
               obstacle_id = message['obstacle'][0]

               # Assicurati che la chiave della direzione esista nel dizionario
               if direction not in updated_obstacles_known:
                    updated_obstacles_known[direction] = set()

               updated_obstacles_known[direction].add(obstacle_id)

          obstacles_known[receiver_id] = updated_obstacles_known  # Aggiorna il dizionario originale

          return updated_obstacles_known

     def plot_message_counts(self, sent_count, received_count, save_path='data/n_mex.png'):
          # Extract data for the plot
          cars = list(sent_count.keys())
          sent_messages = list(sent_count.values())
          received_messages = list(received_count.values())

          # Width of the bars
          bar_width = 0.35

          # Position of the bars on the X-axis
          index = np.arange(len(cars))

          # Create the plot
          fig, ax = plt.subplots()
          
          # Set custom colors for bars
          color_sent = 'orange'
          color_received = 'blue'
          
          bars_sent = ax.bar(index, sent_messages, bar_width, label='Sent Messages', color=color_sent)
          bars_received = ax.bar(index + bar_width, received_messages, bar_width, label='Received Messages', color=color_received)

          # Labels, titles, and legends
          ax.set_xlabel('Vehicles')
          ax.set_ylabel('Quantity')
          ax.set_title('Total Count of Sent and Received Messages for Each Vehicle')
          ax.set_xticks(index + bar_width / 2)
          ax.set_xticklabels(cars)
          ax.legend()

          # Display the plot
          plt.savefig(save_path)
          plt.show()
          
     print ('#######################################################\n')
     
     def evaluate_obstacles_visibility(self):
        for car_map_A in self.array_car_map:
            car_A = car_map_A.car
            obstacles_info_A = []

            for car_map_B in self.array_car_map:
                car_B = car_map_B.car

                if car_A != car_B:
                    obstacles_visible_to_A = set(obs.ID for obs, _ in car_A.visible_obs)
                    obstacles_visible_to_B = set(obs.ID for obs, _ in car_B.visible_obs)

                    obstacles_only_visible_to_A = obstacles_visible_to_A - obstacles_visible_to_B

                    if obstacles_only_visible_to_A:
                        obstacles_info_A.append(f"Car {car_A.ID} vede ostacoli che Car {car_B.ID} non vede: {obstacles_only_visible_to_A}")

            if obstacles_info_A:
                print("\n".join(obstacles_info_A))
                
     def evaluate_obstacles_visibility_plot(self, save_path='data/obstacles_visibility_plot.png'):
        vehicles = [car_map.car.ID for car_map in self.array_car_map]
        data = {vehicle: [0] * len(self.array_car_map) for vehicle in vehicles}

        for i, car_map_A in enumerate(self.array_car_map):
            car_A = car_map_A.car

            for j, car_map_B in enumerate(self.array_car_map):
                car_B = car_map_B.car

                if car_A != car_B:
                    obstacles_visible_to_A = set(obs.ID for obs, _ in car_A.visible_obs)
                    obstacles_visible_to_B = set(obs.ID for obs, _ in car_B.visible_obs)

                    obstacles_only_visible_to_A = obstacles_visible_to_A - obstacles_visible_to_B
                    data[car_A.ID][j] = len(obstacles_only_visible_to_A)

        df = pd.DataFrame(data, index=vehicles)

        # Utilizza seaborn per migliorare la visualizzazione
        sns.set(font_scale=1)
        plt.figure(figsize=(8, 6))
        cmap = sns.light_palette("orange", as_cmap=True)
        sns.heatmap(df, annot=True, cmap=cmap, fmt="d", linewidths=.5, cbar_kws={'label': 'Number of obstacles'},
                    square=True, annot_kws={"size": 8}, xticklabels=vehicles, yticklabels=vehicles, cbar=True)
        plt.title("Number of obstacles not seen by each vehicle relative to others")
        plt.xticks(rotation=0, ha="center")
        plt.yticks(rotation=0, va="center")
        plt.tight_layout()

        # Salva l'immagine
        plt.savefig(save_path)
        plt.show()
        
     def evaluate_obstacles_visibility_dir(self):
        for car_map_A in self.array_car_map:
            car_A = car_map_A.car

            for car_map_B in self.array_car_map:
                car_B = car_map_B.car

                if car_A != car_B:
                    obstacles_only_visible_to_A = []
                    obstacles_only_visible_to_B = []

                    for obs_A, dist_A in car_A.visible_obs:
                        if obs_A not in set(obs_B for obs_B, _ in car_B.visible_obs):
                            if (obs_A, dist_A) in car_A.obstacle_north:
                                obstacles_only_visible_to_A.append((obs_A.ID, dist_A, "North"))
                            elif (obs_A, dist_A) in car_A.obstacle_south:
                                obstacles_only_visible_to_A.append((obs_A.ID, dist_A, "South"))
                            elif (obs_A, dist_A) in car_A.obstacle_east:
                                obstacles_only_visible_to_A.append((obs_A.ID, dist_A, "East"))
                            elif (obs_A, dist_A) in car_A.obstacle_west:
                                obstacles_only_visible_to_A.append((obs_A.ID, dist_A, "West"))

                    for obs_B, dist_B in car_B.visible_obs:
                        if obs_B not in set(obs_A for obs_A, _ in car_A.visible_obs):
                            if (obs_B, dist_B) in car_B.obstacle_north:
                                obstacles_only_visible_to_B.append((obs_B.ID, dist_B, "North"))
                            elif (obs_B, dist_B) in car_B.obstacle_south:
                                obstacles_only_visible_to_B.append((obs_B.ID, dist_B, "South"))
                            elif (obs_B, dist_B) in car_B.obstacle_east:
                                obstacles_only_visible_to_B.append((obs_B.ID, dist_B, "East"))
                            elif (obs_B, dist_B) in car_B.obstacle_west:
                                obstacles_only_visible_to_B.append((obs_B.ID, dist_B, "West"))

                    if obstacles_only_visible_to_A:
                        self.save_obstacles_visibility_info(car_A.ID, car_B.ID, obstacles_only_visible_to_A)

                    if obstacles_only_visible_to_B:
                        self.save_obstacles_visibility_info(car_B.ID, car_A.ID, obstacles_only_visible_to_B)

     def save_obstacles_visibility_info(self, car_id_1, car_id_2, obstacles_info):
        if car_id_1 not in self.obstacles_visibility_info:
            self.obstacles_visibility_info[car_id_1] = {}

        if car_id_2 not in self.obstacles_visibility_info[car_id_1]:
            self.obstacles_visibility_info[car_id_1][car_id_2] = obstacles_info

     def get_obstacles_visibility_info(self):
        return self.obstacles_visibility_info
   
     def print_obstacles_visibility_info(self):
        for car_id_1, info_dict in self.obstacles_visibility_info.items():
            for car_id_2, obstacles_info in info_dict.items():
                print(f"Car {car_id_1} sees obstacles that Car {car_id_2} doesn't see:")
                self.print_grouped_obstacles(obstacles_info)

     def print_grouped_obstacles(self, obstacles_info):
        grouped_obstacles = {}
        for obs_info in self:
            direction = obs_info[2]
            if direction not in grouped_obstacles:
                grouped_obstacles[direction] = [(obs_info[0], obs_info[1])]
            else:
                grouped_obstacles[direction].append((obs_info[0], obs_info[1]))

        for direction, obstacles in grouped_obstacles.items():
            print(f"{direction}: {', '.join(f'({obs[0]}, {obs[1]})' for obs in obstacles)}")

     def plot_obstacles_visibility_heatmap(self, save_path='data/heatmap.png'):
        # Creare una lista di tutte le direzioni per ogni car
        directions = ["North", "South", "East", "West"]
        car_directions = [f"{car_map.car.ID}_{direction}" for car_map in self.array_car_map for direction in directions]

        # Creare un DataFrame con il conteggio degli ostacoli per ogni coppia di veicoli e direzione
        data = []
        for car_map_A in self.array_car_map:
            for car_map_B in self.array_car_map:
                if car_map_A.car != car_map_B.car:
                    obstacles_visible_to_A = self.obstacles_visibility_info.get(car_map_A.car.ID, {}).get(car_map_B.car.ID, [])
                    obstacles_visible_to_B = self.obstacles_visibility_info.get(car_map_B.car.ID, {}).get(car_map_A.car.ID, [])

                    for direction in directions:
                        count_A = len([(obs, dist) for obs, dist, obs_direction in obstacles_visible_to_A if obs_direction == direction])
                        count_B = len([(obs, dist) for obs, dist, obs_direction in obstacles_visible_to_B if obs_direction == direction])

                        data.append([f"{car_map_A.car.ID}_{direction}", f"{car_map_B.car.ID}_{direction}", count_A, count_B])

        df = pd.DataFrame(data, columns=["Car_Direction", "Other_Car_Direction", "Count_A", "Count_B"])

        # Creare il plot con seaborn utilizzando una palette di tonalità arancioni
        plt.figure(figsize=(12, 8))
        heatmap_data = df.pivot_table(index="Car_Direction", columns="Other_Car_Direction", values="Count_A", fill_value=0)
        sns.heatmap(heatmap_data, annot=True, cmap="Oranges", cbar_kws={'label': 'Number of Obstacles'})
        plt.title("Obstacles Visibility Heatmap")

        # Salvare l'immagine
        plt.savefig(save_path)

        # Mostrare il plot
        plt.show()
        
     def simulate_communication_uni(self):
          total_messages_sent = 0
          obstacles_known = {car.ID: {'north': set(), 'south': set(), 'east': set(), 'west': set()} for car in self.array_AVs}
          messages_sent_count = {car.ID: 0 for car in self.array_AVs}
          messages_received_count = {car.ID: 0 for car in self.array_AVs}

          for sender_car_map in self.array_car_map:
               sender_id = sender_car_map.car.ID

               for receiver_car_map in self.array_car_map:
                    receiver_id = receiver_car_map.car.ID

                    if sender_id != receiver_id:
                         messages_to_send = self.determine_messages_to_send_uni(sender_car_map, receiver_car_map, obstacles_known)

                         obstacles_known[receiver_id] = self.update_obstacles_known_uni(receiver_car_map, messages_to_send,
                                                                                     obstacles_known[receiver_id])

                         messages_sent_count[sender_id] += len(messages_to_send)
                         messages_received_count[receiver_id] += len(messages_to_send)

                         total_messages_sent += len(messages_to_send)

                         if messages_to_send:
                              print(f"Car {sender_id} sends images to Car {receiver_id}:", messages_to_send)

          for car_id in messages_sent_count.keys():
               print(f"Car {car_id} sends {messages_sent_count[car_id]} messages and receives {messages_received_count[car_id]} messages.")

          print(f"Total messages sent during the simulation: {total_messages_sent}")

          self.plot_message_counts(messages_sent_count, messages_received_count,'data/n_mex_uni.png')

     def determine_messages_to_send_uni(self, sender_car_map, receiver_car_map, obstacles_known):
          messages_to_send = []

          for direction in ['north', 'south', 'east', 'west']:
               obstacles_sender = getattr(sender_car_map.car, f'obstacle_{direction}')
               obstacles_receiver_known = obstacles_known.get(receiver_car_map.car.ID, {}).get(direction, set())

               max_distance_obstacle = max(obstacles_sender, key=lambda x: x[1], default=None)

               if max_distance_obstacle is not None:
                    obs_sender, dist_sender = max_distance_obstacle

                    if obs_sender.ID and obs_sender.ID not in obstacles_receiver_known:
                         messages_to_send.append({'direction': direction, 'obstacle': (obs_sender.ID, dist_sender)})

          return messages_to_send

     def update_obstacles_known_uni(self, receiver_car_map, messages_to_send, obstacles_known):
          receiver_id = receiver_car_map.car.ID
          updated_obstacles_known = obstacles_known.get(receiver_id, {}).copy()

          for message in messages_to_send:
               direction = message['direction']
               obstacle_id = message['obstacle'][0]

               if direction not in updated_obstacles_known:
                    updated_obstacles_known[direction] = set()

               updated_obstacles_known[direction].add(obstacle_id)

          obstacles_known[receiver_id] = updated_obstacles_known

          return updated_obstacles_known
     
     def voi(self):
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
          
          
          ahp_calculator = AHP(matrix)

          print(ahp_calculator.get_weights())
          print('\n')
          print(ahp_calculator.get_consistency_ratio())
          #ahp_calculator.print_report()
          
          conditional_VOI = Conditional_VOI(ahp_calculator)
          values = [5,5,5,0.8]
          print(conditional_VOI.calculate_importance_value(values))
               
