"""
Gilles NGASSAM & Daniel KOANGA
30/12/2024
"""

# Librairies importation
import random as rd
from datetime import time
from enum import Enum
from collections import Counter

# some constraints definitions (time in minutes)
SERVICE_START = 6 * 60
SERVICE_END = 24 * 60
PEAK_TIME_INTERVALS = [(SERVICE_START, 10 * 60), (10 * 60, 16 * 60), (16 * 60, 20 * 60), (20 * 60, SERVICE_END)]

# Define the daytime intervals
class DAYTIME(Enum):
    MORNING = 0
    DAY = 1
    EVENING = 2
    NIGHT = 3

# Generate a random demand sample to evaluate the fitness of a solution
class Demand:
    def __init__(self, boarding_stop: int, waiting_arrival: int, stops: int, direction: bool):
        """
        Initialize a demand object.

        Args:
            boarding_stop (int): the stop where the passenger is waiting (and will board the bus)
            stops (int): the number of stops the passenger will travel
            direction (bool): direction of the bus (True for forward, False for backward)
            boarding_arrival (int): the time at which the passenger arrives at the boarding stop

        Returns:
            Demand: a demand object
        """
        self.boarding_stop = boarding_stop
        self.stops = stops
        self.direction = direction
        self.waiting_arrival = waiting_arrival

    def __repr__(self):
        hours, minutes, seconds = self.waiting_arrival // 3600, (self.waiting_arrival % 3600) // 60, self.waiting_arrival % 60

        return f"\n{"GARE TGV" if self.direction else "VALDOIE "} - boarding stop: {self.boarding_stop} arrival_time: {time(hours, minutes, seconds)} stops: {self.stops}"


# Generate a random demand sample to evaluate the fitness of a solution
def generate_demand_sample(num_stops: int, num_demands: int, peak_repartition: list[(DAYTIME, float)]) -> list[Demand]:
    """
    Generate a random demand sample to evaluate the fitness of a solution.

    Args:
        num_stops (int): number of stops
        num_demands (int): number of demands to generate
        peak_repartition (list[(DAYTIME, float)]): peak constraints with daytime intervals and associated probabilities 

    Returns:
        list[int]: random demand sample representative of the peak repartition
    """
    demand_sample: list[Demand] = []

    # Generate the peak constraints for the whole demand sample
    peak_times = [peak[0] for peak in peak_repartition]
    peak_probabilities = [peak[1] for peak in peak_repartition]
    peak_indicators = rd.choices(peak_times,peak_probabilities , k=num_demands)

    print(Counter(peak_indicators))

    # Process the demand generation
    for index in range(num_demands):
        direction = rd.choice([True, False])

        if direction:
            boarding_stop = rd.randint(1, num_stops - 1)
        else:
            # process the backward direction (from the last stop to the first one)
            # E.g: the stop N°4 will become the stop N°1
            boarding_stop = num_stops - rd.randint(1, num_stops - 1)
        
        stops = rd.randint(1, num_stops - boarding_stop)
        # Implement an asset who make arrival time meets the peak constraints (morning, day, evening and night)
        demand_interval = PEAK_TIME_INTERVALS[peak_indicators[index].value]
        waiting_arrival = rd.randint(demand_interval[0] * 60, demand_interval[1] * 60)  # start and end of the selected peak interval
        
        demand_sample.append(Demand(boarding_stop, waiting_arrival, stops, direction))

    return demand_sample