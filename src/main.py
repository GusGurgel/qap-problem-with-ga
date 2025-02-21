from input_generators import gen_flux_matrix, gen_distance_matrix
from genetic_algorithms import Population, Chromosome

n = 5
distance_matrix = gen_distance_matrix(n)
flux_matrix = gen_flux_matrix(n)

population = Population.random_population(10, n, distance_matrix, flux_matrix)

ps = [ population.select_with_addicted_roulette(0) for x in range(10)]

for p in ps:
    print(p)

c = Chromosome.crossover_with_majority(*ps)
print(c)