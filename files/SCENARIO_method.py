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
import csv


from tabulate import tabulate
import pprint

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
     
     n_obs = 4
     
     # Generate map
     map = Map(intersection, road)
          
     def __init__(self):
          self.array_AVs = self.generate_all_AVs()
          self.array_car_map = self.generate_all_car_map(self.array_AVs)
          self.obs_array = self.generate_obstacles(Simulated_Scenario.n_obs)
          #self.obs_array = self.generate_all_obstacles()
          self.obstacles_visibility_info = {}
          
          # param of scenario
          '''
          self.polygon_spawn
          self.car_data
          self.n_obs
          self.intersection
          self.road
          '''
     
     # BUILD SCENARIO
     # **************************************************************************** #
     
     def generate_all_AVs(self):
          array_AVs = []
          car_data = [
               ('A', 11.007767285707814, 45.439492436628484, 90),
               ('B', 11.007789421555742, 45.43937903284822, 90),
               ('C', 11.007903263242582, 45.439586043947855, 180),
               ('D', 11.007484262837124, 45.43954676351245, 0.1),
               ('E', 11.008225211533869, 45.43960992760452, 180),
               ('F', 11.007983298078727, 45.439737059970014, 270)
               ]
               
          for ID, x, y, orientation in car_data:
               array_AVs.append(Car(ID, x, y, orientation))
                    
          return array_AVs
     
     def generate_all_obstacles(self):
          array_obs = []
          obs_data = [
               ('obs01', 11.007313, 45.439529),
               ('obs02', 11.007481, 45.439583),
               ('obs03', 11.007761, 45.439594)
          ]
          
          for ID, x, y in obs_data:
               array_obs.append(Obstacle(ID, x, y,))
                    
          return array_obs
        
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

     def generate_and_save_obstacles(self, n_obs, output_csv_file="data/obstacles.csv"):
          polygon, polygon_coords = self.generate_spawn_zone()
          obstacle_data = []

          for i in range(n_obs):
               # Genera un punto casuale all'interno del poligono
               while True:
                    x = random.uniform(min(p[0] for p in polygon_coords), max(p[0] for p in polygon_coords))
                    y = random.uniform(min(p[1] for p in polygon_coords), max(p[1] for p in polygon_coords))
                    point = Point(x, y)

                    # Controlla se il punto è all'interno del poligono
                    if polygon.contains(point):
                         break

               # Aggiungi l'ostacolo alla lista
               obstacle_data.append(('obs{:02d}'.format(i + 1), x, y))

          obs_array = []

          for data in obstacle_data:
               obs = Obstacle(data[0], data[1], data[2])
               obs_array.append(obs)

          # Salva i dati degli ostacoli in un file CSV
          with open(output_csv_file, 'w', newline='') as csvfile:
               csv_writer = csv.writer(csvfile)
               csv_writer.writerow(['ID', 'X', 'Y'])  # Scrivi l'intestazione
               for data in obstacle_data:
                    
                    csv_writer.writerow([data[0], data[1], data[2]])


          return obs_array
     
     def load_obstacles_from_csv(self, input_csv_file="data/obstacles.csv"):
        obs_array = []

        # Apre il file CSV contenente i dati degli ostacoli
        with open(input_csv_file, 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)  # Salta la riga dell'intestazione

            for row in csv_reader:
                # Estrae i dati dalla riga
                obs_id, x, y = row
                x, y = float(x), float(y)

                # Crea un oggetto Ostacolo e aggiungilo all'array
                obs = Obstacle(obs_id, x, y)
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
             
     # IMPORTANT
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
     
     # BROADCAST METHOD
     # **************************************************************************** #
     
     def simulate_broadcast_communication_prior(self):
          total_messages_sent = 0
          messages_data = []
          
          # message count
          messages_sent_count = {car.ID: 0 for car in self.array_AVs}
          messages_received_count = {car.ID: 0 for car in self.array_AVs}
          
          # redundancy count
          redundancy_dict = {car.ID: 0 for car in self.array_AVs}
          redundancy_sent_count = {car.ID: 0 for car in self.array_AVs}
          redundancy_received_count = {car.ID: 0 for car in self.array_AVs}

          for sender_car in self.array_AVs:
               sender_id = sender_car.ID

               for receiver_car in self.array_AVs:
                    receiver_id = receiver_car.ID
                    
                    # init condition
                    if receiver_id not in redundancy_dict:
                         redundancy_dict[receiver_car] = [obs.ID for obs, _ in receiver_car.visible_obs]

                    if sender_id != receiver_id:
                         # Determine all images to send from sender to receiver
                         messages_to_send, n_mex = self.determine_messages_to_send_broadcast(sender_car)

                         
                         if n_mex:
                              messages_sent_count[sender_id] += n_mex
                              messages_received_count[receiver_id] += n_mex
                              total_messages_sent += n_mex

                         if messages_to_send:
                              messages_data.append({
                              'Sender_ID': sender_id,
                              'Receiver_ID': receiver_id,
                              'Messages': messages_to_send
                              })
                              
                                   
                              
                         
          obstacle_dictionary = self.create_obstacle_dictionary(messages_data)

          print('obstacle_dictionary',obstacle_dictionary)
          #print('redundant_count',redundant_count)
          # plot and save
          self.plot_mex_counts(messages_sent_count, messages_received_count, 'data/mex_counts_broadcast.png')
          self.save_AV_mex_count(messages_sent_count, messages_received_count, total_messages_sent, 'data/AV_mex_count_broadcast.xlsx')
          self.save_content_communication(messages_data, 'data/content_communication_broadcast.xlsx')

          print(f"Total messages sent during the broadcast simulation: {total_messages_sent}")
     
     def simulate_broadcast_communication(self):
          total_messages_sent = 0
          messages_data = []
          
          # message count
          messages_sent_count = {car.ID: 0 for car in self.array_AVs}
          messages_received_count = {car.ID: 0 for car in self.array_AVs}
          
          # redundancy count
          redundancy_dict = {car.ID: [] for car in self.array_AVs}
          redundancy_sent_count = {car.ID: 0 for car in self.array_AVs}
          redundancy_received_count = {car.ID: 0 for car in self.array_AVs}
          redundancy_count = 0
          
          array = []

          for sender_car in self.array_AVs:
               sender_id = sender_car.ID

               for receiver_car in self.array_AVs:
                    receiver_id = receiver_car.ID
                    
                    redundancy_dict[receiver_id] = [(obs.ID, dist) for obs, dist in receiver_car.visible_obs]

                    array.extend([(obs.ID, dist) for obs, dist in receiver_car.visible_obs])
                    
                    if sender_id != receiver_id:
                         # Determine all images to send from sender to receiver
                         messages_to_send, n_mex = self.determine_messages_to_send_broadcast(sender_car)

                         if n_mex:
                              messages_sent_count[sender_id] += n_mex
                              messages_received_count[receiver_id] += n_mex
                              total_messages_sent += n_mex

                         if messages_to_send:
                              messages_data.append({
                              'Sender_ID': sender_id,
                              'Receiver_ID': receiver_id,
                              'Messages': messages_to_send
                              })
                              
                              # redundant count
                              for data in messages_to_send:
                                   obstacles = data['obstacles']
                                   id_list = [tupla for tupla in obstacles]

                                   # count redundancy
                                   obs_id_unknown = list(set(id_list) - set(redundancy_dict[receiver_id])) 
                                   if not(obs_id_unknown):
                                        redundancy_sent_count[sender_id] += 1 
                                        redundancy_received_count[receiver_id] += 1 
                                        redundancy_count += 1
                                   
                                   redundancy_dict[receiver_id].extend(id_list)

          average_dist = self.average_dist(array)
          redundancy_perc = redundancy_count/total_messages_sent * 100
          
          # PLOT AND SAVE                    
          self.plot_mex_counts(messages_sent_count, messages_received_count, 'data/mex_counts_broadcast.png')
          self.save_AV_mex_count(messages_sent_count, messages_received_count, total_messages_sent, 'data/AV_mex_count_broadcast.xlsx')
          self.save_content_communication(messages_data, 'data/content_communication_broadcast.xlsx')


          #pprint.pprint(self.average_dist(array))
          #print(f"Total messages sent during the broadcast simulation: {total_messages_sent}")
          
          # PRINT
          print('********************')
          print('BRODCAST SIMULATION')
          print('********************')
          print('Total messages:', total_messages_sent)
          print('Average value: {:.2f}'.format(average_dist))
          print('Redundancy count: ', redundancy_count)
          print('Redundancy {:.2f}%'.format(redundancy_perc))
          
     def average_dist(self,lista_tuple):
          dist_minime_per_obs = {}
          
          for obs_id, dist in lista_tuple:
               # Se l'obs_id non è presente nel dizionario o la distanza è minore di quella memorizzata, aggiorna il valore
               if obs_id not in dist_minime_per_obs or dist < dist_minime_per_obs[obs_id][1]:
                    dist_minime_per_obs[obs_id] = (obs_id, dist)
                    
          
          distanze_minime = [dist for _, dist in dist_minime_per_obs.values()]
          media = sum(distanze_minime) / len(distanze_minime) if len(distanze_minime) > 0 else 0
          
          return media

     # this
     def mean_score(self, list):
          sum_score = sum(dist for _ , dist in list)
          mean_score = sum_score / (len(list))
          
          return mean_score     

     # private     
     def determine_messages_to_send_broadcast(self, sender_car):
          messages_to_send = []
          n_added_directions = 0

          for direction in ['north', 'south', 'east', 'west']:
               sender_obstacle_ids = {obs.ID: dist for obs, dist in sender_car.visible_obs}

               n_added_directions += 1

               unique_obstacles_tupla = [(obs.ID, dist) for obs, dist in sender_car.visible_obs if obs.ID in sender_obstacle_ids]

               direction_data = {'direction': direction, 'obstacles': unique_obstacles_tupla}
               messages_to_send.append(direction_data)

          return messages_to_send, n_added_directions
     
     
     # NAIVE METHOD
     # **************************************************************************** #
     # every AV checks the obstacles derected from the other. 
     # It sends to everyone in need the info about their missing obs
     
     '''
     * questo metodo considera l'invio delle info degli ostacoli che non sono visti dal ricevitore.
     * se in una direzione ci sono più ostacoli di questo tipo vengono comunque conteggiati come singolo invio (dovuto dalla 
     * direzione). Sarebbe possibile contare ogni singolo invio modidicando il conteggio con le seguenti:
     * ' messages_sent_count[sender_id] += len(messages_to_send)
     *   messages_received_count[receiver_id] += len(messages_to_send) '
     *   e sistema 'total_messages_sent'
     '''
     
     def simulate_naive_communication(self):
          total_messages_sent = 0
          messages_data = []

          messages_sent_count = {car.ID: 0 for car in self.array_AVs}
          messages_received_count = {car.ID: 0 for car in self.array_AVs}
          
          array_dict = {car.ID: [] for car in self.array_AVs}

          # redundancy count
          redundancy_dict = {car.ID: set() for car in self.array_AVs}
          redundancy_sent_count = {car.ID: 0 for car in self.array_AVs}
          redundancy_received_count = {car.ID: 0 for car in self.array_AVs}
          redundancy_count = 0
          
          for receiver_car in self.array_AVs:
               receiver_id = receiver_car.ID
               redundancy_dict[receiver_id] = [(obs.ID, dist) for obs, dist in receiver_car.visible_obs]
               
          #print('**********')
          
          #pprint.pprint(redundancy_dict)
          
          #print('**********')

          for sender_car in self.array_AVs:
               sender_id = sender_car.ID
               

               for receiver_car in self.array_AVs:
                    receiver_id = receiver_car.ID
                                        
                    if sender_id != receiver_id:
                         # Determine which obstacles the sender should send to the receiver in each direction
                         messages_to_send, n_mex = self.determine_messages_to_send_naive(sender_car, receiver_car)
                                                                         
                         if n_mex:
                              messages_sent_count[sender_id] += n_mex
                              messages_received_count[receiver_id] += n_mex
                              total_messages_sent += n_mex
                              
                         if messages_to_send:
                              messages_data.append({
                                   'Sender_ID': sender_id,
                                   'Receiver_ID': receiver_id,
                                   'Messages': messages_to_send 
                              })
                              
                         
                         for data in messages_to_send:
                              obs_unknown = []
                              obstacles = data['obstacles']
                              
                              
                              tupla_list = [tupla for tupla in obstacles]
                              tupla_list_id = [tupla[0] for tupla in obstacles]
                              
                              redundancy_dict_id = [tupla[0] for tupla in redundancy_dict[receiver_id]]
                              
                              obs_unknown = list(set(tupla_list_id) - set(redundancy_dict_id))
                              
                              if len(obs_unknown) == 0:
                                   redundancy_sent_count[sender_id] += 1 
                                   redundancy_received_count[receiver_id] += 1 
                                   redundancy_count += 1
                              
                              for obs_id in obs_unknown:

                                   for tupla in tupla_list:
                                        if tupla[0] == obs_id:
                                             dist_data = tupla[1]
                              
                                   redundancy_dict[receiver_id].append((obs_id,dist_data))
                                   
                              
                              
                       
                              
                              
          #pprint.pprint(redundancy_dict)       
          #print('media_distanza_tra_tuple',self.media_distanza_tra_tuple(redundancy_dict))   
          #pprint.pprint(self.trova_minore(redundancy_dict))                                                  
          #pprint.pprint(self.average_dist(array))
          
          redundancy_perc = redundancy_count/total_messages_sent * 100
          average_dist = self.media_distanza_tra_tuple(redundancy_dict)
                       
          # plot and save
          self.plot_mex_counts(messages_sent_count, messages_received_count, 'data/mex_counts_naive.png')
          self.plot_mex_counts(redundancy_sent_count, redundancy_received_count, 'data/redundat_mex_counts_broadcast.png')
          self.save_AV_mex_count(messages_sent_count, messages_received_count, total_messages_sent, 'data/AV_mex_count_naive.xlsx')
          self.save_content_communication(messages_data, 'data/content_communication_naive.xlsx')
          
          #print(f"Total messages sent during the naive simulation: {total_messages_sent}")
          
          
          # PRINT
          print('********************')
          print('NAIVE SIMULATION')
          print('********************')
          print('Total messages:', total_messages_sent)
          print('Average value: {:.2f}'.format(average_dist))
          print('Redundancy count: ', redundancy_count)
          print('Redundancy {:.2f}%'.format(redundancy_perc))
          
          
     
     def determine_messages_to_send_naive(self, sender_car, receiver_car):
          messages_to_send = []
          n_added_directions = 0

          receiver_obstacle_ids = {obs.ID for obs, dist in receiver_car.visible_obs}

          for direction in ['north', 'south', 'east', 'west']:
               sender_direction_obs_ids = {obs.ID for obs, dist in getattr(sender_car, f'obstacle_{direction}')}
               unique_obstacle_ids = sender_direction_obs_ids - receiver_obstacle_ids

               if unique_obstacle_ids:  # Check if there are unique obstacles for the current direction
                    n_added_directions += 1

                    unique_obstacles_tupla = [(obs.ID, dist) for obs, dist in getattr(sender_car, f'obstacle_{direction}') if obs.ID in unique_obstacle_ids]

                    direction_data = {'direction': direction, 'obstacles': unique_obstacles_tupla}
                    messages_to_send.append(direction_data)

          return messages_to_send, n_added_directions
     
     
     def media_distanza_tra_tuple(self,dizionario):
          # Inizializza le variabili per la somma delle distanze e il conteggio delle tuple
          somma_distanze = 0
          conteggio_tuple = 0
          
          # Itera attraverso il dizionario
          for lista_tuple in dizionario.values():
               # Itera attraverso la lista di tuple
               for tupla in lista_tuple:
                    # Aggiunge la distanza della tupla alla somma delle distanze
                    somma_distanze += tupla[1]
                    # Incrementa il conteggio delle tuple
                    conteggio_tuple += 1
          
          # Calcola la distanza media
          if conteggio_tuple > 0:
               distanza_media = somma_distanze / conteggio_tuple
          else:
               distanza_media = 0
          
          return distanza_media
     
     def trova_minima_dist(self,array_tuple):
          minime_distanze = {}
          
          for obs_id, dist in array_tuple:
               # Se l'obs_id non è presente nel dizionario o la distanza è minore di quella attualmente registrata,
               # aggiorniamo il valore nel dizionario
               if obs_id not in minime_distanze or dist < minime_distanze[obs_id]:
                    minime_distanze[obs_id] = dist
          
          # Convertiamo il dizionario in una lista di tuple
          risultato = [(obs_id, dist) for obs_id, dist in minime_distanze.items()]
          
          return risultato
     

     
     # MY METHOD OPTIMIZED
     # **************************************************************************** #
     
     def simulate_optimized_communication(self):
          total_messages_sent = 0
          messages_data = []
          messages_sent_count = {car.ID: 0 for car in self.array_AVs}
          messages_received_count = {car.ID: 0 for car in self.array_AVs}
          obs_info, obstacle_dict = self.find_min_distance_directions()

          
          for received_car in self.array_AVs:
               list_obj = []
               #print('received car: ', received_car.ID)

               for obs_ID in obs_info.keys():
                    if obs_ID not in [obs_c.ID for obs_c, dist in received_car.visible_obs]:
                         list_obj.append(obs_ID)

               car_direction_pairs = set()
               processed_pairs = set()  

               for obs_ID in list_obj:
                    for (sender_car, direction), obs_info_list in obstacle_dict.items():
                         for obs, dist in obs_info_list:
                              if obs == obs_ID and (sender_car, direction) not in processed_pairs:
                                   car_direction_pairs.add((sender_car, direction))
                                   processed_pairs.add((sender_car, direction))
                                   

               #print('car_direction_pairs',car_direction_pairs)
               
               
               for (sender_car, direction) in car_direction_pairs: #(key = sender_car, direction)
                    if (sender_car, direction) in obstacle_dict:
                         content = obstacle_dict[(sender_car, direction)]
                         # print('content',content)
                         # print(f"Key: {(sender_car, direction)}, Content: {content}")
                                   
                         messages_data.append({
                              'Sender_ID': sender_car,
                              'Receiver_ID': received_car.ID,
                              'Messages': content
                         })
                         
                         messages_sent_count[sender_car] += 1  
                         messages_received_count[received_car.ID] += 1
                         total_messages_sent += 1
                         
          average_dist, unique_obstacles_dict = self.create_unique_obstacles_dict_opt(messages_data)
          #print('unique_obstacles_dict',unique_obstacles_dict)
          # plot and save
          self.plot_mex_counts(messages_sent_count, messages_received_count, 'data/mex_counts_optimize.png')
          self.save_AV_mex_count(messages_sent_count, messages_received_count, total_messages_sent, 'data/AV_MEX_counts_optimize.xlsx')
          self.save_content_communication(messages_data, 'data/content_communication_mex_counts_optimize.xlsx')
          
          #print(f"Total messages sent during the optimized simulation: {total_messages_sent}")
          
          
          # PRINT
          print('********************')
          print('OPTIMIZES SIMULATION')
          print('********************')
          print('Total messages:', total_messages_sent)
          print('Average value: {:.2f}'.format(average_dist))


     # min dist
     def find_min_distance_directions(self):
          obs_info = {}

          for car in self.array_AVs:
               for tupla in car.visible_obs:
                    obs, dist = tupla[0], tupla[1]
                    
                    if (obs.ID not in obs_info or obs_info[obs.ID][2] > dist):
                         direction = car.get_direction(tupla)
                         obs_info[obs.ID] = [car.ID, direction, dist]

                    #elif(obs_info[obs.ID][2] > dist):
                    #     obs_info[obs.ID] = [car.ID, direction, dist]
                    
                    direction = ('fail')
               
          return (obs_info, self.construct_obstacle_dictionary(obs_info))
     
     def construct_obstacle_dictionary(self,obs_info):
          obstacle_dict = {}

          for obs_id, info_list in obs_info.items():
               
               car_id, direction, dist = info_list
               key = (car_id, direction)

               if key not in obstacle_dict:
                    obstacle_dict[key] = []

               obstacle_dict[key].append((obs_id, dist))
          
          return obstacle_dict
     
     def create_unique_obstacles_dict_opt(self,messages_data):
          unique_obstacles_dict = {car.ID: [] for car in self.array_AVs}

          for received_car in self.array_AVs:
               unique_obstacles_tupla = set()

               # Add obstacle tuples from visible_obs
               for obs_c, dist in received_car.visible_obs:
                    unique_obstacles_tupla.add((obs_c.ID, dist))

               # Add obstacle tuples from received messages
               for message_data in messages_data:
                    if message_data['Receiver_ID'] == received_car.ID:
                         for content_obs, content_dist in message_data['Messages']:
                              unique_obstacles_tupla.add((content_obs, content_dist))

               # Convert the set to a list and sort by distance
               unique_obstacles_list = sorted(list(unique_obstacles_tupla), key=lambda x: x[1])

               # Add the list to the dictionary
               unique_obstacles_dict[received_car.ID] = unique_obstacles_list

          average_dist = self.calculate_average_distance_opt(unique_obstacles_dict)
          return average_dist, unique_obstacles_dict

     def calculate_average_distance_opt(self, unique_obstacles_dict):
          total_distance = 0
          total_count = 0

          for car_id, obstacles_list in unique_obstacles_dict.items():
               for _, distance in obstacles_list:
                    total_distance += distance
                    total_count += 1

          if total_count == 0:
               return 0  # To avoid division by zero if there are no obstacles

          average_distance = total_distance / total_count
          #print(f"Average distance of unique obstacles opt: {average_distance}")

          return average_distance
     
     # PLOT & SAVE METHODS
     # **************************************************************************** #

     # png
     def plot_mex_counts(self, sent_count, received_count, save_path='data/mex_counts.png'):
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
     
     # to exel
     def save_AV_mex_count(self, messages_sent_count, messages_received_count, total_messages_sent, filename = 'data/AV_mex_count.xlsx'):
          # Create a DataFrame with the data to be saved
          data = [{'Car_ID': car_id, 'Messages_Sent': sent_count, 'Messages_Received': received_count}
                    for car_id, sent_count, received_count in zip(messages_sent_count.keys(),
                                                                 messages_sent_count.values(),
                                                                 messages_received_count.values())]

          # Add a row for the total messages
          total_data = {'Car_ID': 'Total', 'Messages_Sent': total_messages_sent, 'Messages_Received': total_messages_sent}
          data.append(total_data)

          df = pd.DataFrame(data)

          # Save the DataFrame to an Excel file
          
          df.to_excel(filename, index=False)
          
     # to exel
     def save_content_communication(self, messages_data, filename='data/content_communication.xlsx'):
        messages_df = pd.DataFrame(messages_data)
        messages_df.to_excel(filename, index=False)
             
     # private
     def create_obstacle_dictionary(self, messages_data):
          obstacle_dictionary = {}

          for car in self.array_AVs:
               car_id = car.ID
               unique_obstacles_dict = {obs.ID: dist for obs, dist in car.visible_obs}

               # Also consider messages received
               for message_data in messages_data:
                    sender_id = message_data['Sender_ID']
                    receiver_id = message_data['Receiver_ID']
                    messages = message_data['Messages']

                    if receiver_id == car_id:
                         for direction_data in messages:
                              if direction_data['direction'] in ['north', 'south', 'east', 'west']:
                                   for obs_id, dist in direction_data['obstacles']:
                                        if obs_id not in unique_obstacles_dict or dist < unique_obstacles_dict[obs_id]:
                                             unique_obstacles_dict[obs_id] = dist

               obstacle_dictionary[car_id] = list(unique_obstacles_dict.items())
               
          self.calculate_average_distances(obstacle_dictionary)
          return obstacle_dictionary
     
     # private
     def calculate_average_distances(self, obstacle_dictionary):
          car_averages = {}

          for car_id, obstacles_list in obstacle_dictionary.items():
               total_distance = sum(dist for _, dist in obstacles_list)
               average_distance = total_distance / len(obstacles_list) if len(obstacles_list) > 0 else 0
               car_averages[car_id] = average_distance

          total_average_distance = sum(car_averages.values()) / len(car_averages) if len(car_averages) > 0 else 0

          # Print individual averages and total average
          for car_id, average_distance in car_averages.items():
               print(f"Average Distance for Car {car_id}: {average_distance}")

          print(f"Total Average Distance: {total_average_distance}")

          return car_averages, total_average_distance
          
     # **************************************************************************** #

     def plot_communication_stats(self, broadcast_file, naive_file, optimized_file):
        # Carica i dati dai file Excel specifici
        broadcast_data = pd.read_excel(broadcast_file)
        naive_data = pd.read_excel(naive_file)
        optimized_data = pd.read_excel(optimized_file)

        # Calcola il numero totale di pacchetti scambiati per ciascun tipo di comunicazione
        broadcast_pacchetti = len(broadcast_data)
        naive_pacchetti = len(naive_data)
        optimized_pacchetti = len(optimized_data)

        # Crea un grafico a barre per il numero di pacchetti scambiati per ciascun tipo di comunicazione
        tipi_comunicazione = ['Broadcast', 'Naive', 'Optimized']
        numero_pacchetti = [broadcast_pacchetti, naive_pacchetti, optimized_pacchetti]

        plt.bar(tipi_comunicazione, numero_pacchetti, color=['blue', 'orange', 'green'])
        plt.xlabel('Tipo di Comunicazione')
        plt.ylabel('Numero di Pacchetti Scambiati')
        plt.title('Numero di Pacchetti Scambiati per Tipo di Comunicazione')
        plt.show()

     # only plot    
     def evaluate_obstacles_visibility(self):
          for car_A in self.array_AVs:
               obstacles_info_A = []
               
               for car_B in self.array_AVs:

                    if car_A != car_B:
                         obstacles_visible_to_A = set(obs.ID for obs, _ in car_A.visible_obs)
                         obstacles_visible_to_B = set(obs.ID for obs, _ in car_B.visible_obs)

                         obstacles_only_visible_to_A = obstacles_visible_to_A - obstacles_visible_to_B

                         if obstacles_only_visible_to_A:
                              obstacles_info_A.append(f"Car {car_A.ID} sees obstacles that {car_B.ID} does not: {obstacles_only_visible_to_A}")

               if obstacles_info_A:
                    print("\n".join(obstacles_info_A))
     
     # generate table terminal and 'visibility_table' 
     def evaluate_obstacles_visibility_table(self):
          av_ids = [car.ID for car in self.array_AVs]
          visibility_table = []

          for car_A in self.array_AVs:
               obstacles_info_A = []

               for car_B in self.array_AVs:
                    if car_A != car_B:
                         obstacles_visible_to_A = set(obs.ID for obs, _ in car_A.visible_obs)
                         obstacles_visible_to_B = set(obs.ID for obs, _ in car_B.visible_obs)

                         obstacles_only_visible_to_A = obstacles_visible_to_A - obstacles_visible_to_B

                         if obstacles_only_visible_to_A:
                              obstacles_info_A.append((car_B.ID, len(obstacles_only_visible_to_A)))

               row = [car_A.ID] + [0] * len(av_ids)
               for av_B, num_obstacles in obstacles_info_A:
                    index_B = av_ids.index(av_B) + 1
                    row[index_B] = num_obstacles

               visibility_table.append(row)

          return av_ids, visibility_table
     
     #plot tabular table
     def print_tabular_table(self):
          
          av_ids, visibility_table = self.evaluate_obstacles_visibility_table()
          table_header = [''] + av_ids
          print(tabulate(visibility_table, headers=table_header, tablefmt='grid'))
          
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
     
     # useless          
     def plot_sns_obs(self, save_path='data/obstacles_visibility_plot.png'):
          vehicles = [car_map.car.ID for car_map in self.array_car_map]
          data = {vehicle: [0] * len(self.array_car_map) for vehicle in vehicles}

          for i, car_A in enumerate(self.array_AVs):

               for j, car_map_B in enumerate(self.array_car_map):
                    car_B = car_map_B.car

                    if car_A != car_B:
                         obstacles_visible_to_A = set(obs.ID for obs, _ in car_A.visible_obs)
                         obstacles_visible_to_B = set(obs.ID for obs, _ in car_B.visible_obs)

                         obstacles_only_visible_to_A = obstacles_visible_to_A - obstacles_visible_to_B
                         data[car_A.ID][j] = len(obstacles_only_visible_to_A)

          df = pd.DataFrame(data, index=self.array_AVs)

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
               