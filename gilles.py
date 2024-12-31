from datetime import datetime, time
from src.models.stations import generate_time_matrix
from src.models.demand import generate_demand_sample
from src.models.stations import process_global_waiting_time
from src.models.stations import Bus_Slot
from src.models.demand import DAYTIME


time_matrix = generate_time_matrix(4)

peak_repartition = [(DAYTIME.MORNING, 35), (DAYTIME.DAY, 15), (DAYTIME.EVENING, 35), (DAYTIME.NIGHT, 15)]

demands = generate_demand_sample(time_matrix.__len__() + 1, 10, peak_repartition)


solution: list[Bus_Slot] = [
    Bus_Slot(time(7,0,0), True), 
    Bus_Slot(time(12, 0, 0), True), 
    Bus_Slot(time(19, 0, 0), True),
    Bus_Slot(time(8,0,0), False), 
    Bus_Slot(time(12, 0, 0), False), 
    Bus_Slot(time(19, 0, 0), False),
]

print(process_global_waiting_time(solution, demands, time_matrix))