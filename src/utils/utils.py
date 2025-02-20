from math import sqrt

def euclidian_distance(p1, p2):
    """
    Retonar a **distância euclidiana entre** p1 e p2
    """

    d_x = pow(abs(p1[0] - p2[0]), 2)
    d_y = pow(abs(p1[1] - p2[1]), 2)
    return sqrt(d_x + d_y)