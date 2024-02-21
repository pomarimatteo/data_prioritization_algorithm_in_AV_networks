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

    '''
    def n_obstacles_value(self,n):
        k_obstacles = 10
        n_max_obstacles = 50
        return f.n_obstacles_function(n, k_obstacles, n_max_obstacles)
    

    def proximity_function(self,dist):
        d0_proximity = 20
        k_proximity = 0.5
        return f.proximity_function(dist, d0_proximity, k_proximity)

    def accuracy_value(self,accuracy):
        return f.accuracy_function(accuracy)
    '''
 
    def calculate_importance_value(self, values):
        '''
        dist_n = values[0]
        n = values[1]
        dist = values[2]
        accuracy = values[3]
        '''
        
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
    
    