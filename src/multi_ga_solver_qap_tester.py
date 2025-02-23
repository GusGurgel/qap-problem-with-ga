# Este script executa e compara dois arquivos JSON de entrada utilizando o GASolverQAP.
# O usuário deve fornecer os nomes de dois arquivos JSON localizados na pasta 'ga_inputs' e o número de execuções (maior que 1).
# O script gera as mesmas matrizes de distância e fluxo para ambos os arquivos, garantindo comparabilidade.
# No final, exibe a média de melhora do algoritmo guloso e o tempo médio de execução para cada arquivo.

import time
import argparse
import csv
from datetime import datetime
from genetic_algorithms import GASolverQAP
from os.path import join, splitext
from config import MAIN_PATH
from statistics import mean
from input_generators import gen_distance_matrix, gen_flux_matrix

def main():
    parser = argparse.ArgumentParser(description="Executa e compara dois arquivos de entrada JSON usando GASolverQAP.")
    parser.add_argument("input_json1", type=str, help="Nome do primeiro arquivo JSON dentro da pasta ga_inputs")
    parser.add_argument("input_json2", type=str, help="Nome do segundo arquivo JSON dentro da pasta ga_inputs")
    parser.add_argument("times", type=int, help="Quantidade de vezes que a entrada será testada (deve ser maior que 1)")
    parser.add_argument("--verbose", action="store_true", help="Exibe detalhes da execução")
    
    args = parser.parse_args()
    
    if args.times < 2:
        print("Erro: O número de execuções deve ser maior que 1.")
        return
    
    input_path1 = join(MAIN_PATH, "ga_inputs", args.input_json1)
    input_path2 = join(MAIN_PATH, "ga_inputs", args.input_json2)

    input_row1 = []
    input_row2 = []
    
    solver1 = GASolverQAP.from_json_file(input_path1)
    solver2 = GASolverQAP.from_json_file(input_path2)
    
    input_distance_matrix = [gen_distance_matrix(solver1.n) for _ in range(args.times)]
    input_flux_matrix = [gen_flux_matrix(solver1.n) for _ in range(args.times)]
    
    results = {args.input_json1: {'greedy_increase': [], 'time': []},
               args.input_json2: {'greedy_increase': [], 'time': []}}
    
    for i in range(args.times):
        print(f"Executando teste {i+1}/{args.times}")
        
        for solver, input_path, key, index in [(solver1, input_path1, args.input_json1, 0), (solver2, input_path2, args.input_json2, 1)]:
            # solver = GASolverQAP.from_json_file(input_path)
            solver.distance_matrix = input_distance_matrix[i]
            solver.flux_matrix = input_flux_matrix[i]
            
            start_time = time.time()
            val = solver.run(verbose=args.verbose)
            elapsed_time = time.time() - start_time
            
            greedy_res = solver.generations[-1].report()["greedy_solution_distance_percent"]
            
            if index == 0:
                input_row1.append([i+1, val._genes, val.fitness])
            else:
                input_row2.append([i+1, val._genes, val.fitness])
            
            results[key]['time'].append(elapsed_time)
            results[key]['greedy_increase'].append(float(greedy_res.replace("%", "")))

    for key in results:
        print(f"\n{key} teve uma média de melhora do algoritmo guloso em {mean(results[key]['greedy_increase']):.2f}%")
        print(f"Tempo médio de execução: {mean(results[key]['time']):.4f} segundos")
    
    csv_path1 = join("ga_outputs", splitext(args.input_json1)[0] + datetime.now().strftime("%y%m%d%H%M") + "_out.csv")
    csv_path2 = join("ga_outputs", splitext(args.input_json2)[0] + datetime.now().strftime("%y%m%d%H%M") + "_out.csv")
    for path, rows in [(csv_path1, input_row1), (csv_path2, input_row2)]:
        with open(path, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["excution_number", "best_genes", "best_fitness"])  # Cabeçalho
            for row in rows:
                writer.writerow(row)
        print(f"Path {path} saved ✅")    


if __name__ == "__main__":
    main()