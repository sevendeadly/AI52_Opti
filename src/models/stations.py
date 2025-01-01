"""
Gilles NGASSAM & Daniel KOANGA
30/12/2024
"""

# Librairies importation
import random as rd
import numpy as np
from datetime import time
from src.models.plan import Prog
from src.models.demand import Demand
from src.utils.time import convertTimeStamp
from src.utils.constants import MIN_TIME_BETWEEN_STOPS, MAX_TIME_BETWEEN_STOPS, SERVICE_END

# Generate a traveling time's array between two consecutives stops
def generate_time_matrix(num_stops: int) -> list[int]:
    """
    Generate an array with time between two consecutives stops in order to represent the whole tour.

    Args:
        num_stops (int): number of stops

    Returns:
        list[int]: array with time between two consecutives stops
    """
    traveling_times_array: list[int] = np.zeros(num_stops - 1)

    for bus_stop in range(num_stops - 1):
        traveling_times_array[bus_stop] = rd.randint(MIN_TIME_BETWEEN_STOPS, MAX_TIME_BETWEEN_STOPS) * 60

    return traveling_times_array


# Calculate the total waiting time for a given schedule
def process_global_waiting_time(
        solution : list[Prog], 
        passengers_demand: list[Demand], 
        time_matrix: list[int], 
        locomotion_capacity: int
    ) -> int:
    """
    Calculate the total waiting time for a given schedule.

    Args:
        solution (list[Prog]): schedule to evaluate
        passengers_demand (list[Demand]): list of passengers demand
        time_matrix (list[int]): list of time intervals between each stop
        locomotion_capacity (int): capacity of each locomotion

    Returns:
        int: total waiting time
    """
    total_waiting_time: int = 0
    current_passengers_demand: list[Demand] = passengers_demand.copy()
    current_passengers_on_board: list[Demand] = []

    for slot in solution:
        # print(slot)
        for step in range(time_matrix.__len__() + 1):
            bus_arrival_time = slot.process_tour_start() + sum(time_matrix[0: step])
            current_stop = step + 1
            # print(f"Stop: {current_stop} - Time: {convertTimeStamp(int(bus_arrival_time))}")
            passengers_on_time = [
                demand for demand in current_passengers_demand if 
                (
                    demand.boarding_stop == current_stop and
                    demand.direction == slot.direction and
                    demand.waiting_arrival < bus_arrival_time
                )
            ]

            # At each stop, decrease the number of stops for the passengers on board
            for passenger in current_passengers_on_board:
                passenger.stops -= 1

            # passengers who have reached their destination get off the bus
            current_passengers_on_board = [
                passenger for passenger in current_passengers_on_board if passenger.stops > 0
            ]

            # take only the passengers that can board the bus in the limit of the bus capacity
            passengers_to_board = passengers_on_time[:(locomotion_capacity - current_passengers_on_board.__len__())]

            # update the number of passengers on board
            current_passengers_on_board += passengers_to_board

            for passenger in passengers_to_board:
                # calculate the waiting time for the passenger
                waiting_time = min(bus_arrival_time - passenger.waiting_arrival, SERVICE_END * 60 - passenger.waiting_arrival)
                # add it to the global time
                total_waiting_time += waiting_time

                # remove the boarded passenger from the current_passengers_demand
                current_passengers_demand.remove(passenger)

    # For the remaining passengers, consider they will wait until the end of the service
    for passenger in current_passengers_demand:
        waiting_time = SERVICE_END * 60 - passenger.waiting_arrival
        total_waiting_time += waiting_time

    # print("No served passengers : ", current_passengers_demand.__len__())

    return total_waiting_time