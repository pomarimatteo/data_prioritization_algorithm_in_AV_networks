from frames_file_handler import Frames_File_Handler
from car import Car
import os
from PIL import Image

class Car_Frames:

    def __init__(self, frames_file_handler, car):
        self.frames_file_handler = frames_file_handler
        self.car = car
        self.front_image = None
        self.back_image = None
        self.left_image = None
        self.right_image = None

        # Carica le immagini dalla cartella data/selma/sc_01
        self.load_images()

    def load_images(self):
        folder_path = "data/selma/sc_01"

        # Lista di nomi di file per ciascuna immagine
        image_files = {
            "front": "front_sc_01.jpg",
            "back": "back_sc_01.jpg",
            "left": "left_sc_01.jpg",
            "right": "right_sc_01.jpg"
        }

        for direction, filename in image_files.items():
            image_file_path = os.path.join(folder_path, filename)

            # Carica l'immagine
            image = Image.open(image_file_path)

            # Assegna l'immagine alla variabile corrispondente
            setattr(self, f"{direction}_image", image)
            print(f"Immagine {direction.capitalize()} caricata con successo da {filename}.")
