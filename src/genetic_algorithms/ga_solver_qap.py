import json

from config import GRID_SIZE

class GASolverQAP:
    # Constants
    SELECTION_WITH_ADDICTED_ROULETTE = 0
    SELECTION_WITH_TOURNAMENT = 1

    CROSSOVER_WITH_TWO_POINTS = 0
    CROSSOVER_WITH_WITH_MAJORITY = 1

    MUTATION_WITH_GLOBAL_SWAP = 0
    MUTATION_WITH_LOCAL_SWAP = 1

    ELITISM_WITH_ONLY_BEST = 0
    ELITISM_WITH_ADDICTED_ROULETTE = 1


    def __init__(self, n:int=15, 
                 selection_function: int = SELECTION_WITH_ADDICTED_ROULETTE,
                 crossover_function: int = CROSSOVER_WITH_TWO_POINTS,
                 mutation_function: int = MUTATION_WITH_GLOBAL_SWAP,
                 elitism_function: int = ELITISM_WITH_ONLY_BEST,
                 mutation_prob = 0.01,
                 generation_limit = 10):
        """
        n: Tamanho do problema QAP
        selection_function: Função de seleção
        crossover_function: Função de crossover
        mutation_function: Função de mutação
        elitism_function: Função de elitismo
        mutation_prob: Probabilidade de mutação
        generation_limit: Limite de geração (critério de parada)
        """
        	
        if n > GRID_SIZE:
            raise ValueError()

        self.n = n
        self.selection_function = selection_function
        self.crossover_function = crossover_function
        self.mutation_function = mutation_function
        self.elitism_function = elitism_function
        self.mutation_prob = mutation_prob
        self.generation_limit = generation_limit
        
    def __str__(self):
        str_selection_function = "SELECTION_WITH_ADDICTED_ROULETTE" if self.selection_function == GASolverQAP.SELECTION_WITH_ADDICTED_ROULETTE else "SELECTION_WITH_TOURNAMENT"
        str_crossover_function = "CROSSOVER_WITH_TWO_POINTS" if self.crossover_function == GASolverQAP.CROSSOVER_WITH_TWO_POINTS else "CROSSOVER_WITH_WITH_MAJORITY"
        str_mutation_function = "MUTATION_WITH_GLOBAL_SWAP" if self.mutation_function == GASolverQAP.MUTATION_WITH_GLOBAL_SWAP else "MUTATION_WITH_LOCAL_SWAP"
        str_elitism_function = "ELITISM_WITH_ONLY_BEST" if self.elitism_function == GASolverQAP.ELITISM_WITH_ONLY_BEST else "ELITISM_WITH_ADDICTED_ROULETTE"

        return f"""GASolverQAP Configuration:
        n = {self.n}
        selection_function = {str_selection_function}
        crossover_function = {str_crossover_function}
        mutation_function = {str_mutation_function}
        elitism_function = {str_elitism_function}
        mutation_prob = {self.mutation_prob}
        generation_limit = {self.generation_limit}
        """

    
    @staticmethod
    def from_json_file(path):
        with open(path, "r") as file:
            data = json.load(file)

        # Mapeando os valores do JSON para os atributos da classe
        selection_function = GASolverQAP.SELECTION_WITH_ADDICTED_ROULETTE if data["selection_function"] in [0, "SELECTION_WITH_ADDICTED_ROULETTE"] else GASolverQAP.SELECTION_WITH_TOURNAMENT
        crossover_function = GASolverQAP.CROSSOVER_WITH_TWO_POINTS if data["crossover_function"] in [0, "CROSSOVER_WITH_TWO_POINTS"] else GASolverQAP.CROSSOVER_WITH_WITH_MAJORITY
        mutation_function = GASolverQAP.MUTATION_WITH_GLOBAL_SWAP if data["mutation_function"] in [0, "MUTATION_WITH_GLOBAL_SWAP"] else GASolverQAP.MUTATION_WITH_LOCAL_SWAP
        elitism_function = GASolverQAP.ELITISM_WITH_ONLY_BEST if data["elitism_function"] in [0, "ELITISM_WITH_ONLY_BEST"] else GASolverQAP.ELITISM_WITH_ADDICTED_ROULETTE

        # Criando uma instância da classe com os valores lidos do JSON
        return GASolverQAP(
            n=data["n"],
            selection_function=selection_function,
            crossover_function=crossover_function,
            mutation_function=mutation_function,
            elitism_function=elitism_function,
            mutation_prob=data["mutation_prob"],
            generation_limit=data["generation_limit"]
        )
    
