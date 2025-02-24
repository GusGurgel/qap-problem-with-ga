from pprint import pformat, pprint
import json

from utils import print_line,  make_line
from config import GRID_SIZE
from genetic_algorithms import Population, Chromosome
from input_generators import gen_distance_matrix, gen_flux_matrix


class GASolverQAP:
    # Constants
    SELECTION_WITH_ADDICTED_ROULETTE = 0
    SELECTION_WITH_TOURNAMENT = 1

    CROSSOVER_WITH_TWO_POINTS = 0
    CROSSOVER_WITH_MAJORITY = 1

    MUTATION_WITH_GLOBAL_SWAP = 0
    MUTATION_WITH_LOCAL_SWAP = 1

    ELITISM_WITH_ONLY_BEST = 0
    ELITISM_WITH_ADDICTED_ROULETTE = 1

    def __init__(
        self,
        n: int = 15,
        selection_function: int = SELECTION_WITH_ADDICTED_ROULETTE,
        crossover_function: int = CROSSOVER_WITH_TWO_POINTS,
        mutation_function: int = MUTATION_WITH_GLOBAL_SWAP,
        elitism_function: int = ELITISM_WITH_ONLY_BEST,
        mutation_prob=0.01,
        generation_limit=10,
        generation_size=100,
        distance_matrix=None,
        flux_matrix=None,
        tournament_size=3,
        crossover_majority_size=3,
    ):
        """
        n: Tamanho do problema QAP
        selection_function: Função de seleção
        crossover_function: Função de crossover
        mutation_function: Função de mutação
        elitism_function: Função de elitismo
        mutation_prob: Probabilidade de mutação
        generation_limit: Limite de geração (critério de parada)
        generation_size: Tamanho de cada geração
        distance_matrix: Matriz de distância
        flux_matrix: Matrix de fluxo
        tournament_size: Sé a função de seleção for torneio isso mostra
        o tamanho do torneio
        crossover_majority_size: Sé a função de crossover for por maioria
        de genes então isso dita a quantidade de pais envolvidos no
        crossoveer
        """

        # if n > GRID_SIZE:
        #     raise ValueError()

        self.n = n
        self.selection_function = selection_function
        self.crossover_function = crossover_function
        self.mutation_function = mutation_function
        self.elitism_function = elitism_function
        self.mutation_prob = mutation_prob
        self.generation_limit = generation_limit
        self.tournament_size = tournament_size
        self.crossover_majority_size = crossover_majority_size

        if distance_matrix == None:
            self.distance_matrix = gen_distance_matrix(self.n)
        else:
            self.distance_matrix = distance_matrix

        if flux_matrix == None:
            self.flux_matrix = gen_flux_matrix(self.n)
        else:
            self.flux_matrix = flux_matrix

        self.generation_size = generation_size
        self.generations: list[Population] = []

    def _reset(self):
        """
        Reseta os solver para poder ser rodado (run) novamente
        """

        self.generations = []

    def run(self, verbose: bool = False) -> Chromosome:
        """
        Roda o solver de QAP com os parâmetros passados

        verbose: Sé True então o processo vai printar informações extras
        como indivíduo com mais/menos fitness e fitness médio da geração
        """

        # Variáveis para os 3 potinhos usado no verbose
        i_spinner = 0
        spinner = ['🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚', '🕛']

        # Reseta o solver
        self._reset()

        inital_population = Population.random_population(
            self.generation_size, self.n, self.distance_matrix, self.flux_matrix
        )

        self.generations.append(inital_population)
        if verbose:
            print(f"Generation [{len(self.generations)}] (created) {spinner[i_spinner%len(spinner)]}")
            i_spinner += 1

        old_generation: Population = self.generations[0]


        # Gerar as gerações até bater o limite (critério de parada)
        while len(self.generations) < self.generation_limit:
            # Criar nova geração
            new_generation = Population(
                distance_matrix=self.distance_matrix, flux_matrix=self.flux_matrix
            )

            # Cria a nova população baseada na geração anterior
            while len(new_generation.chromosomes) < self.generation_size:
                partners: list[Chromosome] = []
                if self.crossover_function == GASolverQAP.CROSSOVER_WITH_TWO_POINTS:
                    # Nessa caso do crossover  de dois pontos precisamos apenas
                    # de dois pais.  # Então meio que fazemos essa "gambiarra"
                    # de usar a # variável de crossover_majority_size para dizer
                    # que a # quantidade de pais é 2
                    self.crossover_majority_size = 2

                # Seleciona os pais da geração antiga
                while len(partners) < self.crossover_majority_size:
                    if (
                        self.selection_function
                        == GASolverQAP.SELECTION_WITH_ADDICTED_ROULETTE
                    ):
                        partners.append(old_generation.select_with_addicted_roulette())
                    else:
                        partners.append(
                            old_generation.select_with_tournament(self.tournament_size)
                        )

                # Adicionar novo Chromosom(o/os) a populacão
                if self.crossover_function == GASolverQAP.CROSSOVER_WITH_TWO_POINTS:
                    c1, c2 = Chromosome.crossover_with_two_points(*partners)
                    # Aplicar mutação
                    if self.mutation_function == GASolverQAP.MUTATION_WITH_LOCAL_SWAP:
                        c1.mutation_swap_two_local(self.mutation_prob)
                        c2.mutation_swap_two_local(self.mutation_prob)
                    else:
                        c1.mutation_swap_two_global(self.mutation_prob)
                        c2.mutation_swap_two_global(self.mutation_prob)
                    new_generation.chromosomes.append(c1)
                    # Em caso de já atingir limite de chromosomos na geração
                    if len(new_generation.chromosomes) >= self.generation_size:
                        break
                    new_generation.chromosomes.append(c2)
                else:
                    c = Chromosome.crossover_with_majority(*partners)
                    # Aplicar mutação
                    if self.mutation_function == GASolverQAP.MUTATION_WITH_LOCAL_SWAP:
                        c.mutation_swap_two_local(self.mutation_prob)
                    else:
                        c.mutation_swap_two_global(self.mutation_prob)
                    new_generation.chromosomes.append(c)

            # Aplicar o elitismo na população
            if self.elitism_function == GASolverQAP.ELITISM_WITH_ONLY_BEST:
                new_generation = Population.elitism_only_best(
                    self.generation_size, old_generation, new_generation
                )
            else:
                new_generation = Population.elitism_addicted_roulette(
                    self.generation_size, old_generation, new_generation
                )

            # Adicionar nova geração
            self.generations.append(new_generation)
            if verbose:
                print(f"Generation [{len(self.generations)}] (created) {spinner[i_spinner%len(spinner)]}")
                i_spinner += 1
            # A geração nova vira a antiga
            old_generation = new_generation

        # Retonar melhor indivíduo da populacão
        return self.generations[-1].chromosomes[0]

    def get_generations_report(self):
        """
        Pegar string de todas as gerações junto com os seus reports
        """

        out = ""

        for i, generation in enumerate(self.generations):
            out += make_line() + "\n"
            out += f"Generation [{i+1}]" + '\n'
            report = generation.report()
            for key in report.keys():
                out += f"- {key}: {report[key]}"  + '\n'
        out += make_line() + "\n"

        return out

    def print_generations_report(self, step=False):
        """
        Printar todas as gerações junto com os seus reports
        """

        for i, generation in enumerate(self.generations):
            print_line()
            print(f"Generation [{i+1}]")
            report = generation.report()
            for key in report.keys():
                print(f"- {key}: {report[key]}")
            if step:
                input()
        print_line()

    def __str__(self):
        str_selection_function = (
            "SELECTION_WITH_ADDICTED_ROULETTE"
            if self.selection_function == GASolverQAP.SELECTION_WITH_ADDICTED_ROULETTE
            else "SELECTION_WITH_TOURNAMENT"
        )
        str_crossover_function = (
            "CROSSOVER_WITH_TWO_POINTS"
            if self.crossover_function == GASolverQAP.CROSSOVER_WITH_TWO_POINTS
            else "CROSSOVER_WITH_WITH_MAJORITY"
        )
        str_mutation_function = (
            "MUTATION_WITH_GLOBAL_SWAP"
            if self.mutation_function == GASolverQAP.MUTATION_WITH_GLOBAL_SWAP
            else "MUTATION_WITH_LOCAL_SWAP"
        )
        str_elitism_function = (
            "ELITISM_WITH_ONLY_BEST"
            if self.elitism_function == GASolverQAP.ELITISM_WITH_ONLY_BEST
            else "ELITISM_WITH_ADDICTED_ROULETTE"
        )
        str_distance_matrix = pformat(self.distance_matrix)
        str_flux_matrix = pformat(self.flux_matrix)

        return f"""n = {self.n}
selection_function = {str_selection_function}
crossover_function = {str_crossover_function}
mutation_function = {str_mutation_function}
elitism_function = {str_elitism_function}
mutation_prob = {self.mutation_prob}
generation_limit = {self.generation_limit}
generation_size = {self.generation_size}
tournament_size = {self.tournament_size}
crossover_majority_size {self.crossover_majority_size}
distance_matrix =
{str_distance_matrix}
str_flux_matrix =
{str_flux_matrix}"""

    @staticmethod
    def from_json_file(path):
        with open(path, "r") as file:
            data = json.load(file)
        
        return GASolverQAP.from_json(data)

    @staticmethod
    def from_json(data : dict):

        # Mapeando os valores do JSON para os atributos da classe
        selection_function = (
            GASolverQAP.SELECTION_WITH_ADDICTED_ROULETTE
            if data["selection_function"] in [0, "SELECTION_WITH_ADDICTED_ROULETTE"]
            else GASolverQAP.SELECTION_WITH_TOURNAMENT
        )
        crossover_function = (
            GASolverQAP.CROSSOVER_WITH_TWO_POINTS
            if data["crossover_function"] in [0, "CROSSOVER_WITH_TWO_POINTS"]
            else GASolverQAP.CROSSOVER_WITH_MAJORITY
        )
        mutation_function = (
            GASolverQAP.MUTATION_WITH_GLOBAL_SWAP
            if data["mutation_function"] in [0, "MUTATION_WITH_GLOBAL_SWAP"]
            else GASolverQAP.MUTATION_WITH_LOCAL_SWAP
        )
        elitism_function = (
            GASolverQAP.ELITISM_WITH_ONLY_BEST
            if data["elitism_function"] in [0, "ELITISM_WITH_ONLY_BEST"]
            else GASolverQAP.ELITISM_WITH_ADDICTED_ROULETTE
        )
        distance_matrix = data["distance_matrix"] if "distance_matrix" in data else None
        flux_matrix = data["flux_matrix"] if "flux_matrix" in data else None

        tournament_size = data["tournament_size"] if "tournament_size" in data else 3
        crossover_majority_size = (
            data["crossover_majority_size"] if "crossover_majority_size" in data else 3
        )

        # Criando uma instância da classe com os valores lidos do JSON
        return GASolverQAP(
            n=data["n"],
            selection_function=selection_function,
            crossover_function=crossover_function,
            mutation_function=mutation_function,
            elitism_function=elitism_function,
            mutation_prob=data["mutation_prob"],
            generation_limit=data["generation_limit"],
            generation_size=data["generation_size"],
            distance_matrix=distance_matrix,
            flux_matrix=flux_matrix,
            tournament_size=tournament_size,
            crossover_majority_size=crossover_majority_size,
        )
