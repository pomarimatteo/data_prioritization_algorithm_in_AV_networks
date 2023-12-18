from SELMA_frames_file_handler import FramesFileHandler
from AHP_conditional_VOI import Conditional_VOI

class AHP_values:
    
    path = '/Users/matteo/Documents/UNIPD/MAGISTRALE/THESIS/CODE/data/segmentation/sc_01/back_sc_01.json'
    file = FramesFileHandler(path)
    print(file.group_objects_by_type_dist)
    
    counts_by_type = file.group_objects_by_type()

    file.print_grouped_by_type(counts_by_type)
    
AHP_values()
