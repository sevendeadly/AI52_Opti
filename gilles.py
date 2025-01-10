from src.algorithms.AG import GeneticAlgorithm
from src.algorithms.SA import SimulatedAnnealing
from src.models.stations import generate_time_matrix, process_global_waiting_time
from src.models.demand import generate_demand_sample, save_demand_as_instance, load_demand_from_instance
from src.models.plan import process_required_locomotions, save_plan_csv, Prog, generate_derivated_plan
from src.models.demand import DAYTIME, Demand
from src.utils.constants import LOCOMOTION_CAPACITY, NUM_LOCOMOTIONS
from datetime import time
import pandas as pd
from src.algorithms.TS import TabuSearch
from src.algorithms.ACO import AntColonyOptimization
from src.algorithms.PSO import ParticleSwarmOptimization

time_matrix = generate_time_matrix(4)

peak_repartition = [(DAYTIME.MORNING, 35), (DAYTIME.DAY, 20), (DAYTIME.EVENING, 35), (DAYTIME.NIGHT, 10)]

# demands = generate_demand_sample(time_matrix.__len__() + 1, 5000, peak_repartition)

# save_demand_as_instance(demands, 'instance_1')

demands = load_demand_from_instance('instance_1')

# ts = TabuSearch(8, 1000, 100, NUM_LOCOMOTIONS, LOCOMOTION_CAPACITY, time_matrix, demands, peak_repartition, 3600)
# ga = GeneticAlgorithm(100, 10, 0.7, 0.1, 0.8, passengers_demand=demands*1, time_matrix=time_matrix)
sa = SimulatedAnnealing(10000, 0.05, 50, 1000, demands*1, time_matrix)
# aco = AntColonyOptimization(5, 100, 2, 1, 0.1, demands*1, time_matrix)
# pso = ParticleSwarmOptimization(100, 100, 0.5, 1, 1, demands*1, time_matrix)
best_solution = sa.optimize()

print("Best solution : ")
best_solution.sort(key=lambda prog: prog.direction)
for prog in best_solution:
    print(prog)

# save_plan_csv(best_solution, 'plan')
print("Global waiting time : ", sa.process_solution_fitness(best_solution))
print("Proposed slots : ", best_solution.__len__())
print("Locomotions needed :  ", process_required_locomotions(best_solution).__len__())