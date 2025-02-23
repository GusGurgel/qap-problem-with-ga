# Esse script possuí testes da parte zero do trabalho onde devemos 
# avaliar e melhor escolha de parâmetros generation_limit, generation_size
# mutation_prob...
from os.path import realpath, dirname, abspath, join
from sys import path

MAIN_PATH = abspath(join(realpath(dirname(__file__)), ".."))
path.append(MAIN_PATH)

from os.path import splitext
from utils import print_line
import time
import csv
from datetime import datetime
from genetic_algorithms import GASolverQAP
from os.path import join
from statistics import mean
from input_generators import gen_distance_matrix, gen_flux_matrix

times = 20
input_file = "input1.json"
input_path = join(MAIN_PATH, "ga_inputs", input_file)
# vals = [3, 5, 10,  *[x*5 for x in range(3, 20)]]
# vals = [3, 5, 10, 15, 20]
# print(vals)
vals = [0.0001, 0.0005, 0.0009, 0.001, 0.005, 0.009, 0.01, 0.02, 0.03, 0.04, 0.05]
# attr_name = "generation_size"
# attr_name = "generation_limit"
# attr_name = "crossover_majority_size"
# attr_name = "tournament_size"
attr_name = "mutation_prob"
iteration = 1
running = True
time_limit = 60
n = 10

inputs = []

for i in range(times):
    inputs.append([gen_distance_matrix(n), gen_flux_matrix(n)])

# Criar o nome do arquivo
filename = f"{attr_name}_n_{n}_t_{times}_tl_{time_limit}_" + splitext(input_file)[0] + datetime.now().strftime("%y%m%d%H%M") + "_out.csv"
filename = join("expecific_tests", filename)

# Criar e escrever o cabeçalho no CSV antes de iniciar o loop
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow([attr_name, "media_ganho_guloso", "media_tempo_execucao"])  # Cabeçalho

for val in vals:
    greedy_increase_arr = []
    time_arr = []

    for i in range(times):
        print(f"running {i+1}/{times}")
        solver = GASolverQAP.from_json_file(input_path)
        setattr(solver, attr_name, val) 
        solver.distance_matrix = inputs[i][0]
        solver.flux_matrix = inputs[i][1]
        n = solver.n
        
        start_time = time.time()  # Começar a contar aqui
        solver.run(verbose=False)
        end_time = time.time()  # Terminar a contagem aqui
        
        elapsed_time = end_time - start_time
        time_arr.append(elapsed_time)
        
        greedy_res = solver.generations[-1].report()["greedy_solution_distance_percent"]
        greedy_increase_arr.append(float(greedy_res.replace("%", "")))

        if elapsed_time > time_limit:
            running = False
            break
    if not running:
        break

    # Calcular médias
    media_ganho = mean(greedy_increase_arr)
    media_tempo = mean(time_arr)

    print_line()
    print(f"Iteração {iteration} utilizando {attr_name}={val}")
    print(f"{input_file} teve uma média de melhora do algoritmo guloso em {media_ganho:.2f}%")
    print(f"Tempo médio de execução: {media_tempo:.2f} segundos")
    print_line()

    # Salvar no CSV imediatamente após cada iteração
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([val, media_ganho, media_tempo])
