from input_generators import gen_flux_matrix, gen_distance_matrix
from genetic_algorithms import Population, Chromosome
from random import uniform

n = 5
distance_matrix = gen_distance_matrix(n)
flux_matrix = gen_flux_matrix(n)

population1 = Population.random_population(5, n, distance_matrix, flux_matrix)
population2 = Population.random_population(5, n, distance_matrix, flux_matrix)
population3 = Population.elitism_addicted_roulette(5, population1, population2)

print(population1)
print(population2)
print(population3)

# p1 = population.select_with_addicted_roulette()
# p2 = population.select_with_tournament(3)

# c1 : Chromosome = Chromosome.crossover_with_two_points(p1, p2)[0]
# c2 : Chromosome = Chromosome.crossover_with_majority(p1, p2)

# c1.mutation_swap_two_global(0.5)
# c2.mutation_swap_two_local(0.5)

# print("PAI 1: ", p1)
# print("PAI 2: ", p2)

# print("FILHO 1: ", c1)
# print("FILHO 2: ", c2)
