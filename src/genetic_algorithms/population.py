from pprint import pformat
from random import sample, choices

from .chromosome import Chromosome


class Population:
    def __init__(self, distance_matrix, flux_matrix):
        # Representa as gerações de chormosos da população.
        #
        # O índice 0 representa a população inicial, o 1
        # a segunda geração e assim por diante
        self.generations: list[list[Chromosome]] = []

        self.distance_matrix = distance_matrix
        self.flux_matrix = flux_matrix

    #---------------------
    # Funções de geração
    #---------------------
    
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
            chromosome = Chromosome(sample(range(n), n), distance_matrix, flux_matrix)
            generation.append(chromosome)

        # Ordernar geração do menor para o maior fitness
        generation = sorted(generation, key=lambda x : x.fitness)

        # Adicionar geração a população
        population.generations.append(generation)

        return population
    
    #---------------------
    # Funções de seleção
    #---------------------

    def select_with_addicted_roulette(self, g: int = 0):
        """
        Seleciona utilizando a metodologia de roleta viciada um indivíduo da
        geração g
        """

        if g < 0 or g >= len(self.generations):
            raise ValueError()

        # Inverter pesos, quanto menor o fitness maior o peso
        fitness_arr = list(map(lambda x : x.fitness,self.generations[g]))
        weights = [1.0 / w for w in fitness_arr]
        sum_weights = sum(weights)
        weights = [w/sum_weights for w in weights]

        # Selecionar um elemento da população utilzando os peso
        return choices(self.generations[g], weights)[0]

    def select_with_tournament(self, n: int, g: int = 0):
        """
        Seleciona utilizando a metodologia de torneio um indivíduo da
        geração g com um torneio de tamanho n
        """

        if n < 0 or g < 0 or g >= len(self.generations):
            raise ValueError()
        
        # Selecionar torneio
        tournament = choices(self.generations[g], k=n)

        # Retornar o com menor fitness
        return min(tournament, key=lambda x : x.fitness)


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
