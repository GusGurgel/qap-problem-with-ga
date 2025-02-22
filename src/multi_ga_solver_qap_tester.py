from genetic_algorithms import GASolverQAP
from os.path import join
from config import MAIN_PATH
from utils import makeline
from qap import resolve_qap_with_greedy


input_path = join(MAIN_PATH, "ga_inputs", "problema_do_relatorio.json")

solver = GASolverQAP.from_json_file(input_path)

resolve_qap_with_greedy(solver.distance_matrix, solver.flux_matrix)

# print(solver)