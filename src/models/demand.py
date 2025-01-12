"""
Gilles NGASSAM & Daniel KOANGA
30/12/2024
"""

# Librairies importation
import random as rd
from datetime import time
from collections import Counter
from src.utils.constants import PEAK_TIME_INTERVALS, DIRECTION_REPARTITION, DEMAND_INSTANCE_HEADERS, UP_TERMINUS, DOWN_TERMINUS
from src.utils.time import DAYTIME, convertTimeStamp
import csv


# Generate a random demand sample to evaluate the fitness of a solution
class Demand:
    def __init__(self, boarding_stop: int, waiting_arrival: int, stops: int, direction: bool):
        """
        Initialize a demand object.

        Args:
            boarding_stop (int): the stop where the passenger is waiting (and will board the locomotion)
            stops (int): the number of stops the passenger will travel
            direction (bool): direction of the vehicle (True for forward, False for backward)
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

        return f"\n{UP_TERMINUS if self.direction else DOWN_TERMINUS} - boarding stop: {self.boarding_stop} arrival_time: {time(hours, minutes, seconds)} stops: {self.stops}"


# Generate a random demand sample to evaluate the fitness of a solution
def generate_demand_sample(num_stops: int, num_demands: int, peak_repartition: list[(DAYTIME, float)]) -> list[Demand]:
    """
    Generate a random demand sample to evaluate the fitness of a solution.

    Args:
        num_stops (int): number of stops
        num_demands (int): number of demands to generate
        peak_repartition (list[(DAYTIME, float)]): peak constraints with daytime intervals and associated probabilities 

    Returns:
        list[Demand]: random demand sample representative of the peak repartition
    """
    demand_sample: list[Demand] = []

    # Generate the peak constraints for the whole demand sample according to time
    peak_times = [peak[0] for peak in peak_repartition]
    peak_probabilities = [peak[1] for peak in peak_repartition]
    peak_indicators = rd.choices(peak_times,peak_probabilities , k=num_demands)

    # Generate the peak constraints according to direction
    directions = rd.choices([True, False], DIRECTION_REPARTITION, k=num_demands)

    print(Counter(peak_indicators))
    print(Counter(directions))

    # Process the demand generation
    for index in range(num_demands):
        direction = directions[index]

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
    
    # Sort the demand according to arrival and direction
    demand_sample.sort(key=lambda demand: (demand.direction, demand.waiting_arrival))

    return demand_sample

# Save a passengers demand as a csv file
def save_demand_as_instance(passengers_demand: list[Demand], file_name: str) -> None:
    """
    Save a passengers demand as a csv file.

    Args:
        passengers_demand (list[Demand]): list of passengers demand
        file_name (str): name of the file to save the demand
    """
    file_location = f'data/instances/{file_name}.csv'
    with open(file_location, 'w', newline='', encoding='utf-8') as csv_file:

        # Create a writer object and set headers
        writer = csv.writer(csv_file)
        writer.writerow(['Arrival time', 'Boarding stop', 'Stops to go', 'Direction'])

        # Save passengers data
        for passenger in passengers_demand:
            direction = UP_TERMINUS if passenger.direction else DOWN_TERMINUS
            waiting_arrival_time = convertTimeStamp(passenger.waiting_arrival)
            writer.writerow([waiting_arrival_time, passenger.boarding_stop, passenger.stops, direction])


# Load passengers demand from csv
def load_demand_from_instance(file_name: str) -> list[Demand]:
    """
    Load passengers demand from csv.

    Args:
        file_name (str): name of the file to load the demand

    Returns:
        list[Demand]: list of passengers demand
    """
    passengers_demands: list[Demand] = []
    file_location = f'data/instances/{file_name}.csv'

    with open(file_location, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Skip the first line (header)
        next(csv_reader)

        # Regenerate demand from each line
        for row in csv_reader:
            boarding_stop = int(row[DEMAND_INSTANCE_HEADERS[1]])
            stops = int(row[DEMAND_INSTANCE_HEADERS[2]])

            arrival_time_string = row[DEMAND_INSTANCE_HEADERS[0]]
            hours, minutes, seconds = map(lambda x: int(x.strip()), arrival_time_string.split(':'))
            arrival_time_seconds = (hours * 3600) + (minutes * 60) + seconds

            direction = row[DEMAND_INSTANCE_HEADERS[3]] == UP_TERMINUS
            demand = Demand( boarding_stop, arrival_time_seconds , stops, direction)

            passengers_demands.append(demand)
    
    # Sort the demand according to arrival and direction
    passengers_demands.sort(key=lambda demand: (demand.direction, demand.waiting_arrival))

    return passengers_demands