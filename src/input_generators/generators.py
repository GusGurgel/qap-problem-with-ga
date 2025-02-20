from random import randint, sample, shuffle
from config import GRID_SIZE, FLUX_RANGE
from utils import euclidian_distance
from math import floor

all_points_cached = []
"""
Isso é uma variável utilizada para guardar em forma de **cache**
todos os índices de GRID_SIZE por GRID_SIZE.

n precisa ser menor que GRID_SIZE*GRID_SIZE. Caso contrário a função
vai retornar um **ValueError**. O mesmo a contece se n for negativo
"""

def gen_random_points(n: int):
    """
    Gera n pontos aleatórios distintos em um grid de tamanho
    GRID_SIZE por GRID_SIZE
    """

    if n < 0:
        raise ValueError("n need to be positive")

    if n > GRID_SIZE*GRID_SIZE:
        raise ValueError("n need to be less than GRID_SIZE*GRID_SIZE")

    all_points = []
    
    if len(all_points_cached) == GRID_SIZE*GRID_SIZE:
        all_points = all_points_cached
    else:
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                all_points.append((i,j))
    
    return sample(all_points, n)

def gen_zero_matrix(n: int):
    """
    Gera uma matriz nula n x n.

    n precisa ser positivo
    """
    if n < 0:
        raise ValueError("'n' need to be positive")

    matrix = []
    for _ in range(0, n):
        matrix.append([0] * n)
    return matrix

def gen_flux_matrix(n: int):
    """
    Gera uma matriz quadrada de fulxo n x n.

    - A parte triangular superior e inferior são iguais
    - A diagonal principal é nula

    n precisa ser positivo, caso contrário a função retonar um ValueError.
    """

    if n < 0:
        raise ValueError("n need to be positive")

    matrix = gen_zero_matrix(n)
    for i in range(n):
        for j in range(n):
            if i != j:
                if matrix[j][i] != 0 or matrix[i][j] != 0:
                    continue
                random_int = randint(*FLUX_RANGE)
                matrix[i][j] = random_int
                matrix[j][i] = random_int
            else:
                matrix[i][j] = 0

    return matrix

def gen_local_matrix(n):
    """
    Gera uma matriz quadrada de fulxo n x n on o índice i,j
    representa a distância de i até j.

    - A parte triangular superior e inferior são iguais
    - A diagonal principal é nula

    'n' precisa ser menor que GRID_SIZE. Caso contrário a função retornarar
    um ValueError. 'n' também precisa ser um valor inteiro.
    """

    if n < 0:
        raise ValueError("'n' need to be positive")

    if n > GRID_SIZE:
        raise ValueError("'n' need to be lass than GRID_SIZE")

    points = gen_random_points(n)
    matrix = gen_zero_matrix(n)

    for i in range(n):
        for j in range(n):
            if i != j:
                if matrix[j][i] != 0 or matrix[i][j] != 0:
                    continue
                dist = floor(euclidian_distance(points[i], points[j]))
                matrix[i][j] = dist
                matrix[j][i] = dist
            else:
                matrix[i][j] = 0
    
    return matrix

def gen_objects_allocation(n):
    """
    Gera uma alocação randômica de n objetos
    """

    arr = [i for i in range(n)]

    shuffle(arr)

    return arr