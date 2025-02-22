from genetic_algorithms import GASolverQAP
from os.path import join
from config import MAIN_PATH
from utils import makeline


solver = GASolverQAP.from_json_file(join(MAIN_PATH, "ga_inputs", "problema_do_relatorio.json"))

print(solver)
res = solver.run()
solver.print_generations_report()
print(res)