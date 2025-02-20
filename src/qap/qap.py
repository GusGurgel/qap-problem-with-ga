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

    