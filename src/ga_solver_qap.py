# Este script executa o algoritmo GASolverQAP utilizando um arquivo JSON como entrada.
# O usuário deve fornecer o nome do arquivo JSON localizado na pasta 'ga_inputs'.
# Opções adicionais incluem:
#   --verbose : Exibe detalhes da configuração e execução.
#   --step    : Exibe o relatório de gerações passo a passo.

import argparse
from genetic_algorithms import GASolverQAP
from os.path import join
from config import MAIN_PATH
from utils import makeline

def main():
    parser = argparse.ArgumentParser(description="Executa o GASolverQAP com um arquivo de entrada JSON.")
    parser.add_argument("input_json", type=str, help="Nome do arquivo JSON dentro da pasta ga_inputs")
    parser.add_argument("--verbose", action="store_true", help="Exibe detalhes da execução")
    parser.add_argument("--step", action="store_true", help="Exibe relatório de gerações passo a passo")
    
    args = parser.parse_args()
    
    input_path = join(MAIN_PATH, "ga_inputs", args.input_json)
    solver = GASolverQAP.from_json_file(input_path)
    
    makeline()
    if args.verbose:
        print("[GASolverQAP Configuration]")
        print(solver)
    else:
        print("[GASolverQAP]")
    
    res = solver.run(verbose=args.verbose)
    
    solver.print_generations_report(step=args.step)
    
    print("[Final Result]")
    print(f"genes: {res._genes}")
    print(f"fitness: {res.fitness}")
    makeline()

if __name__ == "__main__":
    main()
