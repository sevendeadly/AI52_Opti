from src.models.stations import generate_time_matrix
from src.models.demand import generate_demand_sample, Demand

time_matrix = generate_time_matrix(10)

print(time_matrix)

demands = generate_demand_sample(time_matrix.__len__() + 1, 10)

result: Demand = []

for demand in demands:
    if demand.direction:
        result.insert(0, demand)
    else:
        result.append(demand)

print(result)