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

tour_duration = sum(time_matrix)

# print(tour_duration)

# solution: list[Prog] = [
#     Prog(time(7,0,0), tour_duration, True),
#     Prog(time(12, 0, 0), tour_duration, True),
#     Prog(time(19, 0, 0), tour_duration, True),
#     Prog(time(7,45,0), tour_duration, True), 
#     Prog(time(8,24,0), tour_duration, False), 
#     Prog(time(12, 0, 0), tour_duration, False), 
#     Prog(time(19, 0, 0), tour_duration, False),
# ]

# for locomotion in process_required_locomotions(solution):
#     print(locomotion)

# print("Locomotions needed : ", process_required_locomotions(solution).__len__())

# print(process_global_waiting_time(solution, demands, time_matrix))

# ga = GeneticAlgorithm(100, 10, 0.7, 0.1, 0.8, num_slots=60, num_locomotions=NUM_LOCOMOTIONS, locomotion_capacity=LOCOMOTION_CAPACITY, time_matrix=time_matrix, passengers_demand=demands*1)

sa = SimulatedAnnealing(10000, 0.1, 50, 1000, 60, time_matrix, demands*1, NUM_LOCOMOTIONS, LOCOMOTION_CAPACITY)
best_solution = sa.optimize()

print("Best solution : ")
best_solution.sort(key=lambda prog: prog.direction)
for prog in best_solution:
    print(prog)

print("Global waiting time : ", sa.process_solution_fitness(best_solution))
print("Proposed slots : ", best_solution.__len__())
print("Locomotions needed :  ", process_required_locomotions(best_solution).__len__())