from pprint import pformat
from math import floor

from qap import get_qap_total_flux, distinct_fill_qap_array_with_array

from random import choices


class Chromosome:
    def __init__(self, genes, distance_matrix, flux_matrix):
        self._genes = genes

        self.distance_matrix = distance_matrix
        self.flux_matrix = flux_matrix
        
        self.fitness = get_qap_total_flux(self.distance_matrix, self.flux_matrix, self._genes)

    def set_genes(self, genes):
        self._genes = genes
        self.fitness = get_qap_total_flux(
            self._genes, self.distance_matrix, self.flux_matrix
        )

    def to_dict_with_fitness(self):
        """
        Retonar o chromossomo no formato de um dicionário com seus genes
        e seu fitness
        """

        chromosome_dict = {"genes": self._genes, "fitness": self.fitness}

        return chromosome_dict

    def str_with_fitness(self):
        """
        retonar a representação do chormossomo em string com o seu
        fitness
        """

        return pformat(
            self.to_dict_with_fitness()
        )

    def __str__(self):
        return self.str_with_fitness()

    # -----------------------
    # Funções de crossover
    # -----------------------

    @staticmethod
    def crossover_with_two_points(p1, p2):
        """
        Gera dois chromossomos filhos utilizando a técnica de
        crossover com dois points. Os dois pais são divididos
        em três partes. A parte do meio do pai 1 fai para o 
        filho 1 e a parte do meio do pai 2 vai para o filho
        2. O pai 2 é utilizado para completar o filho 1
        e o pai 1 é utilizado para completar o filho 2

        Exemplo
        p1 [1, 2, 3]
        p2 [2, 3, 1]

        c1 = [*, 2, *] -> [3, 2, 1]
        c2 = [*, 3, *] -> [1, 3, 2]
        """
        if len(p1._genes) != len(p2._genes):
            raise ValueError()

        if len(p1._genes) < 3:
            raise ValueError()
        
        l = len(p1._genes)

        split_size = floor(l / 3)

        child1 = [None] * l
        child2 = [None] * l

        # Insere a metade da terça parte de p1 em child1
        # Insere a metade da terça parte de p2 em child2
        for j in range(split_size, 2 * split_size):
            child1[j] = p1._genes[j]
            child2[j] = p2._genes[j]

        # Utiliza p2 para completar child1
        distinct_fill_qap_array_with_array(child1, p2._genes)
        # Utiliza p1 para completar child2
        distinct_fill_qap_array_with_array(child2, p1._genes)


        return Chromosome(child1, p1.distance_matrix, p1.flux_matrix), Chromosome(
            child2, p1.distance_matrix, p1.flux_matrix
        )
    
    def crossover_with_majority(*p):
        """
        Gera um choromosomo filho baseado nos p's cromossomos pais. 
        O cruzamento é feito sorteando um gene da posição i de
        cada pai. O fitness de cada pai é utilizado como peso
        para seleção dos genes. Assim, pais com fitness maior
        possuem maior chance de passar seu gene.
        """

        l = len(p[0]._genes)

        if l < 2:
            raise ValueError()

        # Inverter pesos, quanto menor o fitness maior o peso
        fitness_arr = list(map(lambda x : x.fitness,p))
        weights = [1.0 / w for w in fitness_arr]
        sum_weights = sum(weights)
        weights = [w/sum_weights for w in weights]

        child = []

        for i in range(l):
            genes = []
            for j in range(len(p)):
                genes.append(p[j]._genes[i])
            print(genes)
            child.append(choices(genes, weights, k=1)[0])
        
        return Chromosome(child, p[0].distance_matrix, p[0].flux_matrix)