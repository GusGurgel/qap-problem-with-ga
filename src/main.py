from input_generators import gen_flux_matrix,  gen_distance_matrix, gen_objects_allocation
from qap import get_qap_total_flux
from genetic_algorithms import Population

n = 3
distance_matrix = gen_distance_matrix(n)
flux_matrix = gen_flux_matrix(n)

population = Population.random_population(10, n, distance_matrix, flux_matrix)
print(population)