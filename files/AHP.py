import ahpy
import numpy as np

class AHP:
    
    def __init__(self, matrix):
        self.matrix = matrix
        self.compose_object = ahpy.Compare(name='Compare', comparisons=self.matrix, precision=6, random_index='saaty')
        
    def get_weights(self):
        return self.compose_object.target_weights

    def get_consistency_ratio(self):
        return self.compose_object.consistency_ratio

    def get_report(self):
        return self.compose_object.report(show=True)

    def calculate_priority_weights(self):
        matrix = np.real_if_close(self.matrix)
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        max_eigenvalue_index = np.argmax(eigenvalues)
        principal_eigenvector = eigenvectors[:, max_eigenvalue_index]
        priority_weights = principal_eigenvector / np.sum(principal_eigenvector)
        priority_weights = np.real_if_close(priority_weights)
        return priority_weights
    
    
    # calcolo fatto da me utilizzando gli autovettori 
    '''
    def calculate_priority_weights(matrix):
        # Assicurati che la matrice sia di tipo reale
        matrix = np.real_if_close(matrix)

        # Calcola gli autovettori e gli autovalori
        eigenvalues, eigenvectors = np.linalg.eig(matrix)

        # Trova l'indice dell'autovalore massimo
        max_eigenvalue_index = np.argmax(eigenvalues)

        # Estrai l'autovettore corrispondente all'autovalore massimo
        principal_eigenvector = eigenvectors[:, max_eigenvalue_index]

        # Normalizza l'autovettore principale per ottenere i pesi delle priorità
        priority_weights = principal_eigenvector / np.sum(principal_eigenvector)

        # Assicurati che la parte immaginaria sia rimossa
        priority_weights = np.real_if_close(priority_weights)

        return priority_weights

    # Esempio di utilizzo
    # Sostituisci la seguente matrice con la tua matrice M
    matrix_M = np.array([[1, 9, 3, 3],
                        [1/9, 1, 1/6, 1/8],
                        [1/3, 6, 1, 1],
                        [1/3, 8, 1, 1]
                        ])

    weights = calculate_priority_weights(matrix_M) # i priority_weights corrispondono. N.B. [1] e [3] sono scambiati ma corrispondono perchè la libreria la scambia. Guarda il nome. 
    print("Priority Weights:", weights)
    '''
