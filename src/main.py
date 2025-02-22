from input_generators import gen_flux_matrix, gen_distance_matrix
from genetic_algorithms import Population, GASolverQAP
from os.path import join
from config import MAIN_PATH


print(GASolverQAP.from_json_file(join(MAIN_PATH, "input1.json")))