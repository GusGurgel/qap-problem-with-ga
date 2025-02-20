from pprint import pformat
from random import sample

from .chromosome import Chromosome


class Population:
    @staticmethod
    def random_population(p: int, n: int, distance_matrix, flux_matrix):
        """
        Gerar uma população para um problema de tamanho n com
        a quantidade de chromosomos igual a p.

        A população vai considerar as matrizes de distâncias e fluxos para cálculo
        dos fitness da população

        - p > 0
        - n > 1
        """

        # Testar valores
        if p < 1 or n < 2:
            raise ValueError()

        population = Population(distance_matrix, flux_matrix)
        generation = []

        # Gerar chromososmos da geração inical
        for _ in range(p):
            chromosome = Chromosome(sample(range(n), n))
            generation.append(chromosome)

        # Adicionar geração a população
        population.generations.append(generation)

        return population

    def __init__(self, distance_matrix, flux_matrix):
        # Representa as gerações de chormosos da população.
        #
        # O índice 0 representa a população inicial, o 1
        # a segunda geração e assim por diante
        self.generations: list[list[Chromosome]] = []

        self.distance_matrix = distance_matrix
        self.flux_matrix = flux_matrix

    def to_dict(self):
        """
        Retonar a população em formato de dicionário.

        {
            "generation_0": [
                { genes: [gene1, gene2...]},
                { genes: [gene1, gene2...]},
                ...
            ]
            "generation_1": [
                { genes: [gene1, gene2...]},
                { genes: [gene1, gene2...]},
                ...
            ]
            ...
        }
        """

        population_dict = {}

        for i, generation in enumerate(self.generations):
            population_dict[f"generation_{i}"] = list(
                map(
                    lambda x: x.to_dict_with_fitness(
                        self.distance_matrix, self.flux_matrix
                    ),
                    generation,
                )
            )

        return population_dict

    def __str__(self):
        return pformat(self.to_dict())
