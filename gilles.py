from src.models.stations import generate_time_matrix
from src.models.demand import generate_demand_sample
from src.models.demand import DAYTIME


time_matrix = generate_time_matrix(4)

peak_repartition = [(DAYTIME.MORNING, 35), (DAYTIME.DAY, 15), (DAYTIME.EVENING, 35), (DAYTIME.NIGHT, 15)]

demands = generate_demand_sample(time_matrix.__len__() + 1, 10, peak_repartition)

print(demands)

