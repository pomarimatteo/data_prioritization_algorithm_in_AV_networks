from AHP import AHP
from AHP_conditional_VOI import Conditional_VOI
from AHP_functions import Functions as f

class AHP_score():
    
    #print('AHP_score')
    # the score is calculated based on the given matrix and the paramater of each functions defined in 'Conditional_VOI' class
    
    '''
    a = 9  #  ('roi', 'distance')
    b = 3  # ('distance', 'roi')
    c = 3  #  ('Distance', 'roi')

    
    matrix = {
        ('n_util_obs', 'n_util_obs'): 1,
        ('n_util_obs', 'Distance'): a,
        ('n_util_obs', 'roi'): b,

        ('Distance', 'n_util_obs'): 1/a,
        ('Distance', 'Distance'): 1,
        ('Distance', 'roi'): c,

        ('roi', 'n_util_obs'): 1/b,
        ('roi', 'Distance'): 1/c,
        ('roi', 'roi'): 1,
    }
    '''
    a = 9 # ('roi', 'distance_S')
    b = 7 # ('roi', 'distance_R'): b,
    c = 1/3 # ('distance_S', 'distance_R'): c,
    
    matrix = {
        
        ('roi', 'roi'): 1,
        ('roi', 'distance_S'): a,
        ('roi', 'distance_R'): b,
        
        ('distance_S', 'roi'): 1/a,
        ('distance_S', 'distance_S'): 1,
        ('distance_S', 'distance_R'): c,
        
        ('distance_R', 'roi'): 1/b,
        ('distance_R', 'distance_S'): 1/c,
        ('distance_R', 'distance_R'): 1,
        
    }
    
    ahp_calculator = AHP(matrix)

    
    print(ahp_calculator.get_weights())
    print('\n')
    print(ahp_calculator.get_consistency_ratio())
    print(ahp_calculator.get_report())
    print('check')
    
    
    conditional_VOI = Conditional_VOI(ahp_calculator)
    values = [5,5,5]
    print('cond',conditional_VOI.calculate_importance_value(values))
    
