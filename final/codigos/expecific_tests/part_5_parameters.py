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
from qap import resolve_qap_with_greedy, get_qap_total_flux

inputs_paths = [
    (join(MAIN_PATH, "ga_inputs", "parte1.json"), "Parte 1"),
    (join(MAIN_PATH, "ga_inputs", "parte2.json"), "Parte 2"),
    (join(MAIN_PATH, "ga_inputs", "parte3.json"), "Parte 3"),
    (join(MAIN_PATH, "ga_inputs", "parte4.json"), "Parte 4")
]
solvers = [
    (GASolverQAP.from_json_file(path), name) for path, name in inputs_paths
]
n_vals = [10, *[x*5 for x in range(3, 20)], 150, 200, 250, 300, 400, 500, 700, 800, 900]
matrixes = []
results = []

running = True
time_limit_seconds = 60*30

for n in n_vals:
    matrixes.append([gen_distance_matrix(n), gen_flux_matrix(n)])

# Criar o nome do arquivo
filename = f"teste_parte_5" + datetime.now().strftime("%y%m%d%H%M") + ".csv"
filename = join("expecific_tests/", filename)

# Criar e escrever o cabeçalho no CSV antes de iniciar o loop
with open(filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["n", "parte1", "parte1 fit", "parte2", "parte2 fit", "parte3", "parte3 fit", "parte4", "parte4 fit", "greedy fit"])  # Cabeçalho

for i,n in enumerate(n_vals):
    print(f"running {i+1}/{len(n_vals)}")

    row = [n]

    for solver,name in solvers:
        solver.n = n
        solver.distance_matrix = matrixes[i][0]
        solver.flux_matrix = matrixes[i][1]
    
        start_time = time.time()  # Começar a contar aqui
        res = solver.run(verbose=True)
        end_time = time.time()  # Terminar a contagem aqui
    
        elapsed_time = end_time - start_time
        row.append(f"{elapsed_time:.4f} s")
        row.append(res.fitness)
    
    greedy_res = resolve_qap_with_greedy(matrixes[i][0], matrixes[i][1])
    greedy_fit = get_qap_total_flux(matrixes[i][0], matrixes[i][1], greedy_res)
    row.append(greedy_fit)
    
    # Salvar no CSV imediatamente após cada iteração
    with open(filename, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(row)