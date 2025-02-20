from pprint import pformat

from qap import get_qap_total_flux


class Chromosome:
    def __init__(self, genes):
        self.genes = genes
    
    def get_fitness(self, distance_matrix, flux_matrix):
        return get_qap_total_flux(distance_matrix, flux_matrix, self.genes)
    
    def to_dict_with_fitness(self, distance_matrix, flux_matrix):
        """
        Retonar o chromossomo no formato de um dicionário com seus genes
        e seu fitness
        """

        chromosome_dict = {
            "genes": self.genes,
            "fitness": self.get_fitness(distance_matrix, flux_matrix)
        }

        return chromosome_dict
    
    def str_with_fitness(self, distance_matrix, flux_matrix):
        """
        retonar a representação do chormossomo em string com o seu
        fitness
        """

        return pformat(self.to_dict_with_fitness(distance_matrix, flux_matrix))

