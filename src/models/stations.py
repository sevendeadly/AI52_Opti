"""
Gilles NGASSAM & Daniel KOANGA
30/12/2024
"""

# Librairies importation
import random as rd
import numpy as np

# some constraints definitions (time in minutes)
MIN_TIME_BETWEEN_STOPS = 2
MAX_TIME_BETWEEN_STOPS = 10
BUS_CAPACITY = 50
NUM_BUS = 15
MIN_DEMANDS = 100
MAX_DEMANDS = 200

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