from AHP_functions import Functions as f
from AHP import AHP

class Conditional_VOI:
    
    def __init__(self, AHP):
        self.AHP = AHP
        
    # for novelty i need the value of d 
    # x and k defined here
    def proximity_relation_strength_value(self,dist_S):                               
        d0_novelty = 25
        k_novelty = 0.5
        return f.proximity_relation_strength_function(dist_S, d0_novelty, k_novelty)
    
    def roi_strength_value(self, angle):
        return f. roi_function(angle)
    
    def proximity_relation_strength_value(self,dist_R):                               
        d0_novelty = 25
        k_novelty = 0.5
        return f.proximity_relation_strength_function(dist_R, d0_novelty, k_novelty)

 
    def calculate_importance_value(self, values):
        angle = values[0]
        dist_S = values[1]
        dist_R = values[2]
        
        
        weights_dict = self.AHP.get_weights()
        # extract attributes weights
        roi_weight = weights_dict['roi']
        dist_S_weight = weights_dict['distance_S']
        dist_R_weight = weights_dict['distance_R']
       

        # Get value from conditional VoI
        proximity_relation_strength_value_R = self.proximity_relation_strength_value(dist_R)
        proximity_relation_strength_value_S = self.proximity_relation_strength_value(dist_S)
        roi_strength_value = self.roi_strength_value(angle)

        # Overall VoI
        importance_value = (roi_weight * roi_strength_value +
                            dist_S_weight * proximity_relation_strength_value_S +
                            dist_R_weight * proximity_relation_strength_value_R)

        return importance_value
    
    