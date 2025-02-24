from os.path import realpath, dirname, abspath, join

MAIN_PATH =  abspath(join(realpath(dirname(__file__)), ".."))
"""
Pasta padrão dos scripts
"""

FLUX_RANGE = [1, 10]
"""
Representa a faixa de valores de fluxo que podem ser atribuidas a um objeto
"""

GRID_SIZE = 30
"""
Representa o **tamanho do grid** utilizado para gerar os **pontos/locais** aleatórios
"""

LINE_SIZE = 60
"""
Tamanho da linha padrão utiliza para divisão no CLI
"""

LINE_CHAR = "-"
"""
Caractere utilizado para fazer as linhas de divisória do terminal
"""