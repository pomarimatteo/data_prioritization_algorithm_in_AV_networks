import json
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

class FramesFileHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.load_data()

    def load_data(self):
        try:
            with open(self.file_path, 'r') as file:
                self.data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # Handle JSON decoding error or file not found
            self.data = {}

    def get_obstacle_count(self):
        if self.data:
            return len(self.data)

    def get_obstacle_info(self, image_id):
        if self.data and image_id in self.data:
            return self.data[image_id]

    def get_obstacle_regions(self, image_id):
        obstacle_info = self.get_obstacle_info(image_id)
        if obstacle_info:
            return obstacle_info.get('regions', [])

    def get_person_count(self, image_id):
        regions = self.get_obstacle_regions(image_id)
        if regions:
            return sum(1 for region in regions if region['region_attributes'].get('person'))

    def add_distance_attribute(self, image_id, distance):
        obstacle_info = self.get_obstacle_info(image_id)
        if obstacle_info:
            for region in obstacle_info.get('regions', []):
                region['region_attributes']['distance'] = distance

    def create_dataset(self):
        data_list = []
        for image_id, obstacle_info in self.data.items():
            for region in obstacle_info.get('regions', []):
                data_entry = {
                    'image_id': image_id,
                    'shape_attributes': region['shape_attributes'],
                    'region_attributes': region['region_attributes']
                }
                data_list.append(data_entry)

        dataset = pd.DataFrame(data_list)
        return dataset

    def _draw_polygon_mask(self, image_id):
        regions = self.get_obstacle_regions(image_id)
        if regions:
            fig, ax = plt.subplots()
            for region in regions:
                shape_attributes = region['shape_attributes']
                polygon = Polygon(
                    [(shape_attributes['all_points_x'][i], shape_attributes['all_points_y'][i])
                     for i in range(len(shape_attributes['all_points_x']))],
                    edgecolor='r', facecolor='none'
                )
                ax.add_patch(polygon)

            plt.title('Polygon Mask for Obstacle')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.show()
            
    def draw_rectangle_mask(self, image_id):
        regions = self.get_obstacle_regions(image_id)
        if regions:
            fig, ax = plt.subplots()
            for region_data in regions.values():
                for region in region_data.get('regions', []):
                    shape_attributes = region['shape_attributes']
                    if shape_attributes['name'] == 'rect':
                        x = shape_attributes['x']
                        y = shape_attributes['y']
                        width = shape_attributes['width']
                        height = shape_attributes['height']

                        rect = plt.Rectangle((x, y), width, height, edgecolor='r', facecolor='none')
                        ax.add_patch(rect)

            plt.title('Rectangle Mask for Obstacle')
            plt.xlabel('X-axis')
            plt.ylabel('Y-axis')
            plt.show()







    def save_changes(self):
        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=2)

    def group_objects_by_type(self):
        grouped_by_type = {}
        for image_id, obstacle_info in self.data.items():
            type_groups = {}
            for region in obstacle_info.get('regions', []):
                object_type = region['region_attributes'].get('type')
                object_name = region['region_attributes'].get('name')
                if object_type and object_name:
                    if object_type not in type_groups:
                        type_groups[object_type] = []
                    type_groups[object_type].append(object_name)

            grouped_by_type[image_id] = type_groups

        return grouped_by_type

    def print_grouped_by_type(self, grouped_by_type):
        for image_id, type_groups in grouped_by_type.items():
            print(f"Image ID: {image_id}:")
            for object_type, object_names in type_groups.items():
                print(f"{object_type} = {object_names}")
            print()


