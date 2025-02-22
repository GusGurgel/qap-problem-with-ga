# Este script executa o GASolverQAP várias vezes com um arquivo JSON de entrada.
# O usuário deve fornecer o nome do arquivo JSON localizado na pasta 'ga_inputs' e o número de execuções (maior que 1).
# Opções adicionais incluem:
#   --verbose : Exibe detalhes da execução.

import time
import argparse
from genetic_algorithms import GASolverQAP
from os.path import join
from config import MAIN_PATH
from statistics import mean

def main():
    parser = argparse.ArgumentParser(description="Executa o GASolverQAP com um arquivo de entrada JSON várias vezes.")
    parser.add_argument("input_json", type=str, help="Nome do arquivo JSON dentro da pasta ga_inputs")
    parser.add_argument("times", type=int, help="Quantidade de vezes que a entrada será testada (deve ser maior que 1)")
    parser.add_argument("--verbose", action="store_true", help="Exibe detalhes da execução")
    
    args = parser.parse_args()
    
    if args.times < 2:
        print("Erro: O número de execuções deve ser maior que 1.")
        return
    
    input_path = join(MAIN_PATH, "ga_inputs", args.input_json)
    
    greedy_increase_arr = []
    time_arr = []
    
    for i in range(args.times):
        print(f"running {i+1}/{args.times}")
        solver = GASolverQAP.from_json_file(input_path)
        
        start_time = time.time()  # Começar a contar aqui
        solver.run(verbose=args.verbose)
        end_time = time.time()  # Terminar a contagem aqui
        
        elapsed_time = end_time - start_time
        time_arr.append(elapsed_time)
        
        greedy_res = solver.generations[-1].report()["greedy_solution_distance_percent"]
        greedy_increase_arr.append(float(greedy_res.replace("%", "")))
    
    print(f"{args.input_json} teve uma média de melhora do algoritmo guloso em {mean(greedy_increase_arr):.2f}%")
    print(f"Tempo médio de execução: {mean(time_arr):.4f} segundos")

if __name__ == "__main__":
    main()
