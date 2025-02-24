# README - Execução dos Algoritmos GASolverQAP

## Visão Geral
Este repositório contém dois scripts para executar o algoritmo GASolverQAP, um baseado em um único arquivo de entrada e outro que compara dois arquivos de entrada.

## Requisitos
Antes de executar os scripts, certifique-se de ter instalado:
- Python 3.8+

## Como Executar

### 1. Executando `ga_solver_qap.py`
Este script executa o algoritmo GASolverQAP utilizando um único arquivo JSON como entrada.

**Uso:**
```bash
python ga_solver_qap.py <arquivo_json> [--verbose] [--step] [--save]
```

**Parâmetros:**
- `<arquivo_json>`: Nome do arquivo JSON dentro da pasta `ga_inputs`.
- `--verbose` (opcional): Exibe detalhes da configuração e execução.
- `--step` (opcional): Exibe relatório detalhado de cada geração.
- `--save` (opcional): Salva o resultado na pasta `ga_outputs`.

**Exemplo:**
```bash
python ga_solver_qap.py problema_do_relatorio.json --verbose --save
```

### 2. Executando `multi_ga_solver_qap_tester.py`
Este script executa e compara dois arquivos JSON de entrada utilizando o GASolverQAP.

**Uso:**
```bash
python multi_ga_solver_qap_tester.py <arquivo_json1> <arquivo_json2> <num_execucoes> [--verbose]
```

**Parâmetros:**
- `<arquivo_json1>`: Nome do primeiro arquivo JSON dentro da pasta `ga_inputs`.
- `<arquivo_json2>`: Nome do segundo arquivo JSON dentro da pasta `ga_inputs`.
- `<num_execucoes>`: Número de execuções do algoritmo (deve ser maior que 1).
- `--verbose` (opcional): Exibe detalhes da execução.

**Exemplo:**
```bash
python multi_ga_solver_qap_tester.py parte1.json parte2.json 10 --verbose
```

Após a execução, o script exibe a média de melhora do algoritmo guloso e o tempo médio de execução para cada arquivo. Os resultados são salvos na pasta `ga_outputs` em arquivos CSV.

## Saída dos Resultados
Os resultados são exibidos no terminal e, se a opção `--save` for usada, os arquivos de saída são armazenados na pasta `ga_outputs`.