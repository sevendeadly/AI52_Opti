"""
Gilles NGASSAM & Daniel KOANGA
30/12/2024
"""

# Librairies importation
import random as rd

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

    def __str__(self):
        pass

    def __repr__(self):
        return f"{"Gare TGV" if self.direction else "Valdoie"} : The passenger arrived at the boarding stop {self.boarding_stop} at {self.waiting_arrival} will ride {self.stops} stops.\n"


# Generate a random demand sample to evaluate the fitness of a solution
def generate_demand_sample(num_stops: int, num_demands: int) -> list[Demand]:
    """
    Generate a random demand sample to evaluate the fitness of a solution.

    Args:
        num_stops (int): number of stops
        num_demands (int): number of demands to generate

    Returns:
        list[int]: random demand sample
    """
    demand_sample: list[Demand] = []

    for _ in range(num_demands):
        direction = rd.choice([True, False])

        if direction:
            boarding_stop = rd.randint(1, num_stops - 1)
        else:
            # process the backward direction (from the last stop to the first one)
            # E.g: the stop N°4 will become the spot N°1
            boarding_stop = num_stops - rd.randint(1, num_stops - 1)
        
        stops = rd.randint(1, num_stops - boarding_stop)
        # Implement an asset who make arrival time meets the peak constraints (morning, day, evening and night) 
        waiting_arrival = rd.randint(0, 18 * 60 * 60)  # 6am to 12am
        
        demand_sample.append(Demand(boarding_stop, waiting_arrival, stops, direction))

    return demand_sample