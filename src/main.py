from input_generators import gen_flux_matrix,  gen_local_matrix, gen_objects_allocation
from qap import get_qap_total_flux

n = 30

local_matrix = gen_local_matrix(n)
flux_matrix = gen_flux_matrix(n)
objects_allocation = gen_objects_allocation(n)

print(get_qap_total_flux(local_matrix, flux_matrix, objects_allocation))