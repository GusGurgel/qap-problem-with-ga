from pprint import pformat
from random import sample, choices

from .chromosome import Chromosome


class Population:
    def __init__(self, distance_matrix, flux_matrix):
        # Representa as gerações de chormosos da população.
        #
        # O índice 0 representa a população inicial, o 1
        # a segunda geração e assim por diante
        self.chromosomes: list[Chromosome] = []

        self.distance_matrix = distance_matrix
        self.flux_matrix = flux_matrix

    def to_dict(self):
        """
        Retonar a população em formato de dicionário.

        {
            "chromosomes": [
                { genes: [gene1, gene2...], fitness: x},
                { genes: [gene1, gene2...], fitness: y},
                ...
            ]
        }
        """

        population_dict = {"chromosomes": list(map(lambda x : str(x), self.chromosomes))}

        return population_dict

    def __str__(self):
        return pformat(self.to_dict())

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

        values = range(n)

        # Testar valores
        if p < 1 or n < 2:
            raise ValueError()

        population = Population(distance_matrix, flux_matrix)

        # Gerar chromososmos da geração inical
        for _ in range(p):
            chromosome = Chromosome(sample(values, n), distance_matrix, flux_matrix)
            population.chromosomes.append(chromosome)

        # Ordernar do menor para o maior fitness
        population.chromosomes = sorted(population.chromosomes, key=lambda x : x.fitness)

        return population
    
    #---------------------
    # Funções de seleção
    #---------------------
    def select_with_addicted_roulette(self) -> Chromosome:
        """
        Seleciona utilizando a metodologia de roleta viciada um indivíduo da
        geração g
        """

        # Inverter pesos, quanto menor o fitness maior o peso
        fitness_arr = list(map(lambda x : x.fitness,self.chromosomes))
        weights = [1.0 / w for w in fitness_arr]
        sum_weights = sum(weights)
        weights = [w/sum_weights for w in weights]

        # Selecionar um elemento da população utilzando os peso
        return choices(self.chromosomes, weights)[0]

    def select_with_tournament(self, n: int) -> Chromosome:
        """
        Seleciona utilizando a metodologia de torneio um indivíduo da
        geração g com um torneio de tamanho n
        """

        if n < 0:
            raise ValueError()
        
        # Selecionar torneio
        tournament = choices(self.chromosomes, k=n)

        # Retornar o com menor fitness
        return min(tournament, key=lambda x : x.fitness)

    #---------------------
    # Funções de elitismo
    #---------------------

    @staticmethod
    def elitism_only_best(n, *p):
        """
        Seleciona só os n melhores elementos das populações *p e retorna
        uma nova população com esse melhores
        """

        population = Population(p[0].distance_matrix, p[0].flux_matrix)
        for aux_population in p:
            for aux_chromosome in aux_population.chromosomes:
                population.chromosomes.append(aux_chromosome.copy())

        population.chromosomes = list(sorted(population.chromosomes, key=lambda x: x.fitness))[0:n]

        return population
    
    @staticmethod
    def elitism_addicted_roulette(n, *p):
        """
        Seleciona só os n melhores elementos das populações *p e retorna
        uma nova população com esse melhores
        """

        population = Population(p[0].distance_matrix, p[0].flux_matrix)
        for aux_population in p:
            for aux_chromosome in aux_population.chromosomes:
                population.chromosomes.append(aux_chromosome.copy())

        population.chromosomes = list(sorted(population.chromosomes, key=lambda x: x.fitness))
        
        # Inverter pesos, quanto menor o fitness maior o peso
        fitness_arr = list(map(lambda x : x.fitness,population.chromosomes))
        weights = [1.0 / w for w in fitness_arr]
        sum_weights = sum(weights)
        weights = [w/sum_weights for w in weights]

        population.chromosomes = choices(population.chromosomes, weights=weights, k=n)
        
        population.chromosomes = list(sorted(population.chromosomes, key=lambda x: x.fitness))


        return population