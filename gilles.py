from src.algorithms.AG import GeneticAlgorithm
from src.algorithms.RS import SimulatedAnnealing
from src.models.stations import generate_time_matrix
from src.models.demand import generate_demand_sample
from src.models.plan import process_required_locomotions
from src.models.demand import DAYTIME
from src.utils.constants import LOCOMOTION_CAPACITY, NUM_LOCOMOTIONS

time_matrix = generate_time_matrix(4)

peak_repartition = [(DAYTIME.MORNING, 35), (DAYTIME.DAY, 15), (DAYTIME.EVENING, 35), (DAYTIME.NIGHT, 15)]

demands = generate_demand_sample(time_matrix.__len__() + 1, 20000, peak_repartition)

sa = SimulatedAnnealing(10000, 0.1, 50, 1000, 60, time_matrix, demands*1, NUM_LOCOMOTIONS, LOCOMOTION_CAPACITY)
best_solution = sa.optimize()

print("Best solution : ")
best_solution.sort(key=lambda prog: prog.direction)
for prog in best_solution:
    print(prog)

print("Global waiting time : ", sa.process_solution_fitness(best_solution))
print("Proposed slots : ", best_solution.__len__())
print("Locomotions needed :  ", process_required_locomotions(best_solution).__len__())