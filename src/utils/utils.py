from math import sqrt

def euclidian_distance(p1, p2):
    """
    Retonar a **distância euclidiana entre** p1 e p2
    """

    d_x = pow(abs(p1[0] - p2[0]), 2)
    d_y = pow(abs(p1[1] - p2[1]), 2)
    return sqrt(d_x + d_y)

def distinct_fill_array_with_array(to_fill_arr, fill_arr):
    """
    vai preencher to_fill_arr com os valores d fill_arr

    Exemplo
    to_fill_arr = [1, None, None, 4, 3]
    fill_arr = [3, 2, 1, 4, 5]
    return = [1, 2, 5, 4, 3] 
    """

    l = len(to_fill_arr)
    j = 0
    for i in range(l):
        if to_fill_arr[i] != None:
            continue
        while j < l:
            if fill_arr[j] not in to_fill_arr:
                to_fill_arr[i] = fill_arr[j]
                j += 1
                break
            j += 1