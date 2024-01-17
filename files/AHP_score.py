from AHP import AHP
from AHP_conditional_VOI import Conditional_VOI
from AHP_functions import Functions as f

class AHP_score():
    
    #print('AHP_score')
    # the score is calculated based on the given matrix and the paramater of each functions defined in 'Conditional_VOI' class
    
    
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

    '''
    print(ahp_calculator.get_weights())
    print('\n')
    print(ahp_calculator.get_consistency_ratio())
    #ahp_calculator.print_report()
    print('check')
    '''
    conditional_VOI = Conditional_VOI(ahp_calculator)
    values = [5,5,5,0.8]
    #print(conditional_VOI.calculate_importance_value(values))
    
