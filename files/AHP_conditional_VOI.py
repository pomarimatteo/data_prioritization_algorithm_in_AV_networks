from AHP_functions import Functions as f
from AHP import AHP

class Conditional_VOI:
    
    def __init__(self, AHP):
        self.AHP = AHP
        
    # for novelty i need the value of d 
    # x and k defined here
    def proximity_relation_strength_value(self,dist):                               
        d0_novelty = 20
        k_novelty = 0.5
        return f.proximity_relation_strength_function(dist, d0_novelty, k_novelty)

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
 
    def calculate_importance_value(self, values):
        
        dist_n = values[0]
        n = values[1]
        dist = values[2]
        accuracy = values[3]
        
        weights_dict = self.AHP.get_weights()
        # extract attributes weights
        novelty_weight = weights_dict['Novelty']
        content_weight = weights_dict['Content']
        distance_weight = weights_dict['Distance']
        reliability_weight = weights_dict['Reliability']

        # Get value from conditional VoI
        proximity_relation_strength_value = self.proximity_relation_strength_value(dist_n)
        n_obstacles_value = self.n_obstacles_value(n)
        proximity_value = self.proximity_function(dist)
        accuracy_value = self.accuracy_value(accuracy)

        # Overall VoI
        importance_value = (novelty_weight * proximity_relation_strength_value +
                            content_weight * n_obstacles_value +
                            distance_weight * proximity_value +
                            reliability_weight * accuracy_value)

        return importance_value
    
    