def get_qap_total_flux(distance_matrix, flux_matrix, objects_allocation):
    """
    Rotonar o fluxo total de uma solução QAP (Quadratic Assignment Problem)

    - **distânce**: Matriz de distâncias
    - **flux_matrix**: Matriz de fluxos
    - **objects_alocations**: Vetor com os objetos de 0..n onde objects_alocation[0] = 2
    significa que o objeto 2 foi alocado no local 0
    """

    if len(distance_matrix[0]) != len(flux_matrix[0]):
        raise ValueError("Invalid matrix size")

    if len(distance_matrix[0]) != len(objects_allocation):
        raise ValueError("Objects matrix size error")
    
    total_flux = 0

    # Pares que já foram calculados
    calculaded_pairs = []
    
    for i in range(len(objects_allocation)):
        for j in range(len(objects_allocation)):
            if (j,i) in calculaded_pairs or (i,j) in calculaded_pairs or i == j:
                continue
            travel_cost = distance_matrix[i][j]
            flux_cost = flux_matrix[objects_allocation[i]][objects_allocation[j]]
            total_flux +=  travel_cost * flux_cost 
            calculaded_pairs.append((i, j))

    return total_flux

    
def resolve_qap_array_dups(arr):
    """
    Resolve duplicatas em um array de resolução de uma qap
    """

    l = len(arr)
    filler = [x for x in range(l)]
    j = 0     

    aux = []
    for i in range(l):
        if arr[i] not in aux:
            aux.append(arr[i])
        else:
            while j < len(filler):
                if filler[j] not in arr:
                    arr[i] = filler[j]
                    j += 1
                    break
                j += 1

def distinct_fill_qap_array_with_array(to_fill_arr, fill_arr):
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

def resolve_qap_with_greedy(distance_matrix, flux_matrix):
    """
    Retona uma solução do problema do QAP utilizando o
    algoritmo guloso com heurística **menor fluxo para maior
    distância como heurística**
    """

    total_distance_array = []
    total_flux_array = []

    for i, row in enumerate(distance_matrix):
        total_distance_array.append((i, sum(row)))
    
    for i, row in enumerate(flux_matrix):
        total_flux_array.append((i, sum(row)))
    
    # Ordenar os arrays
    total_distance_array = sorted(total_distance_array, key=lambda x : x[1], reverse=True)
    total_flux_array = sorted(total_flux_array, key=lambda x : x[1])

    # Construir array de resultado
    result_array = [None]*len(total_distance_array)

    for i in range(len(total_distance_array)):
        # índice da i-ésima maior distância
        index = total_distance_array[i][0]
        # o objeto de í-ésimo menor fluxo fica alocado no índice da í-esima
        # maior distância
        result_array[index] = total_flux_array[i][0]
    
    return result_array