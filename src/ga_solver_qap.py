# Este script executa o algoritmo GASolverQAP utilizando um arquivo JSON como entrada.
# O usuário deve fornecer o nome do arquivo JSON localizado na pasta 'ga_inputs'.
# Opções adicionais incluem:
#   --verbose : Exibe detalhes da configuração e execução.
#   --step    : Exibe o relatório de gerações passo a passo.

import argparse
from genetic_algorithms import GASolverQAP
from os.path import join, splitext
from config import MAIN_PATH
from utils import print_line, make_line
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(
        description="Executa o GASolverQAP com um arquivo de entrada JSON."
    )
    parser.add_argument(
        "input_json", type=str, help="Nome do arquivo JSON dentro da pasta ga_inputs"
    )
    parser.add_argument(
        "--verbose", action="store_true", help="Exibe detalhes da execução"
    )
    parser.add_argument(
        "--step", action="store_true", help="Exibe relatório de gerações passo a passo"
    )
    parser.add_argument(
        "--save", action="store_true", help="Salva o resultado na pasta 'ga_outputs'"
    )

    args = parser.parse_args()

    input_path = join(MAIN_PATH, "ga_inputs", args.input_json)
    solver = GASolverQAP.from_json_file(input_path)

    output_txt = ""

    print_line()
    output_txt += make_line() + "\n"
    print("[GASolverQAP Configuration]")
    if args.verbose:
        print(solver)

    print(f"Running:  {args.input_json}")
    output_txt += f"Running:  {args.input_json}" + "\n"
    res = solver.run(verbose=args.verbose)

    solver.print_generations_report(step=args.step)
    output_txt += solver.get_generations_report() + "\n"

    output_txt += "[Final Result]" + "\n"
    print("[Final Result]")
    output_txt += f"genes: {res._genes}" + "\n"
    print(f"genes: {res._genes}")
    output_txt += f"fitness: {res.fitness}" + "\n"
    print(f"fitness: {res.fitness}")
    output_txt += make_line() + "\n"
    print_line()

    if args.save:
        filename = splitext(args.input_json)[0] + datetime.now().strftime("%y%m%d%H%M") + "_out.txt"
        save_path = join(MAIN_PATH, "ga_outputs", filename)
        with open(save_path, "w") as file:
            file.write(output_txt)
        print(f"File {filename} saved ✅")


if __name__ == "__main__":
    main()
