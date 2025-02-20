from pprint import pformat
from random import sample

from .chromosome import Chromosome


class Population:
    @staticmethod
    def random_population(p: int, n: int):
        """
        Gerar uma população para um problema de tamanho n com
        a quantidade de chromosomos igual a p

        - p > 0
        - n > 1
        """

        # Testar valores
        if p < 1 or n < 2:
            raise ValueError()

        population = Population()
        generation = []

        # Gerar chromososmos da geração inical
        for _ in range(p):
            chromosome = Chromosome(sample(range(n), n))
            generation.append(chromosome)
        
        # Adicionar geração a população
        population.generations.append(generation)
        
        return population


    def __init__(self):
        # Representa as gerações de chormosos da população.
        #
        # O índice 0 representa a população inicial, o 1
        # a segunda geração e assim por diante
        self.generations = []
    
    def to_dict(self):
        """
        Retonar a população em formato de dicionário. 

        {
            "generation_0": [[gene1, gene2...], [gene1, gene2...]...]
            "generation_1": [[gene1, gene2...], [gene1, gene2...]...]
            ...
        }
        """

        population_dict = {}

        for i, generation in enumerate(self.generations):
            population_dict[f"generation_{i}"] = list(map(lambda x : x.genes, generation))
        
        return population_dict

    def __str__(self):
        print(pformat(self.to_dict()))