from input_generators import gen_flux_matrix, gen_distance_matrix
from qap import get_qap_total_flux
from genetic_algorithms import Population, Chromosome
from utils import distinct_fill_array_with_array

n = 6
distance_matrix = gen_distance_matrix(n)
flux_matrix = gen_flux_matrix(n)

population = Population.random_population(10, n, distance_matrix, flux_matrix)

p1 = population.select_with_addicted_roulette(0)
p2 = population.select_with_addicted_roulette(0)

c1, c2 = Chromosome.crossover_with_two_points(p1, p2)

print(p1)
print(p2)
print("-"*10)
print(c1)
print(c2)