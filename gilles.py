from datetime import time
from src.algorithms.AG import GeneticAlgorithm
from src.models.stations import generate_time_matrix
from src.models.demand import generate_demand_sample
from src.models.stations import process_global_waiting_time
from src.models.plan import Prog, Locomotion, process_required_locomotions
from src.models.demand import DAYTIME


time_matrix = generate_time_matrix(4)

peak_repartition = [(DAYTIME.MORNING, 35), (DAYTIME.DAY, 15), (DAYTIME.EVENING, 35), (DAYTIME.NIGHT, 15)]

demands = generate_demand_sample(time_matrix.__len__() + 1, 1000, peak_repartition)

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

ga = GeneticAlgorithm(10, 10, 0.8, 0.1, 60, 4, 50, time_matrix, demands)

individual = ga.generate_individual()

for reservation in individual:
    print(reservation)

print("Global waiting time : ",process_global_waiting_time(individual, demands, time_matrix))
print("Locomotions needed :  ", process_required_locomotions(individual).__len__())