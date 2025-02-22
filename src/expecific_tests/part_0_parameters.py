# Esse script possuí testes da parte zero do trabalho onde devemos 
# avaliar e melhor escolha de parâmetros n generation_limit,
from os.path import realpath, dirname, abspath, join
from sys import path

MAIN_PATH = abspath(join(realpath(dirname(__file__)), ".."))
path.append(MAIN_PATH)

from os.path import splitext
import time
from genetic_algorithms import GASolverQAP
from os.path import join
from statistics import mean
    
times = 10
input_file = "input1.json"
input_path = join(MAIN_PATH, "ga_inputs", input_file)

while True:
    greedy_increase_arr = []
    time_arr = []

    for i in range(times):
        print(f"running {i+1}/{times}")
        solver = GASolverQAP.from_json_file(input_path)
        
        start_time = time.time()  # Começar a contar aqui
        solver.run(verbose=True)
        end_time = time.time()  # Terminar a contagem aqui
        
        elapsed_time = end_time - start_time
        time_arr.append(elapsed_time)
        
        greedy_res = solver.generations[-1].report()["greedy_solution_distance_percent"]
        greedy_increase_arr.append(float(greedy_res.replace("%", "")))

    print(f"{input_file} teve uma média de melhora do algoritmo guloso em {mean(greedy_increase_arr):.2f}%")
    print(f"Tempo médio de execução: {mean(time_arr):.2f} segundos")
    break
