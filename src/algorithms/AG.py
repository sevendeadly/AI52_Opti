"""
Gilles NGASSAM & Daniel KOANGA
30/12/2024
"""

"""
Implémente l'Algorithme Génétique pour l'optimisation des horaires de bus.
Gère l'évolution de la population via sélection, croisement et mutation.
Paramètres clés : taille de population, taux de croisement, taux de mutation

Let's assume between midnigh and 6am, there is no bus
"""
# libraries importation
from src.models.plan import Prog, is_valid_plan
from src.models.demand import Demand
from datetime import time
import random as rd
from src.utils.time import convertTimeStamp

# some constraints definitions (time in minutes)
SERVICE_START = 6 * 60
SERVICE_END = 24 * 60

class GeneticAlgorithm:
    # Constructor
    def __init__(
            self, num_generations: int, 
            population_size: int, 
            crossover_rate: float, 
            mutation_rate: float, 
            num_slots: int, 
            num_locomotions: int,
            locomotion_capacity: int,
            time_matrix: list[int],
            passengers_demand: list[Demand]
        ):
        """
        Initialize the Genetic Algorithm with the given parameters

        Args:
            num_generations (int): Number of generations
            population_size (int): Number of individuals in the population
            crossover_rate (float): Probability of crossover
            mutation_rate (float): Probability of mutation
            num_slots (int): Number of time slots in the schedule
            num_locomotions (int): Number of locomotions in the schedule
            locomotion_capacity (int): Capacity of each locomotion
            time_matrix (list[int]): List of time intervals between each stop
            passengers_demand (list[Demand]): List of passengers demand

        Returns:
            None
        """
        self.num_generations = num_generations
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.num_slots = num_slots
        self.num_locomotions = num_locomotions
        self.locomotion_capacity = locomotion_capacity
        self.time_matrix = time_matrix
        passengers_demand = passengers_demand

    # Generate a random individual
    def generate_individual(self) -> list[Prog]:
        """
        Generate a random individual
        
        Returns:
            list[Prog]: a random individual with a proposed schedule
        """
        individual: list[Prog] = []

        while not self.is_valid_individual(individual) or individual.__len__() != self.num_slots:
            # Initialize an empty individual
            individual: list[Prog] = []

            for _ in range(self.num_slots):
                # Generate a random time 
                    # SERVICE_START * 60) + 1 : Served at least 1 second after the start of the service
                    # SERVICE_END * 60) - 1 : Served at least 1 second before the end of the service
                start_time_seconds = int(rd.randint((SERVICE_START * 60) + 1, (SERVICE_END * 60) - 1)) 
                start_time = convertTimeStamp(start_time_seconds)

                # Generate a random direction
                direction = rd.choice([True, False])

                # Create a new Prog instance
                duration = sum(self.time_matrix)
                prog = Prog(start_time, duration, direction)

                # Add the new Prog to the individual
                individual.append(prog)

        # sort the individual by time
        individual.sort(key=lambda prog: prog.time)

        return individual
    
    # Check if an individual is valid according 
    def is_valid_individual(self, individual: list[Prog]) -> bool:
        return is_valid_plan(individual, self.num_locomotions)
        
    def generate_population(self, time_matrix: list[int]) -> list[list[Prog]]:
        pass

    def evaluate_population(self, population: list[list[Prog]], passengers_demand: list[Demand], time_matrix: list[int]) -> list[int]:
        pass

    def select_parents(self, population: list[list[Prog]], fitness_scores: list[int]) -> list[list[Prog]]:
        pass

    def crossover(self, parent1: list[Prog], parent2: list[Prog], crossover_rate: float) -> list[Prog]:
        pass

    def mutate(self, individual: list[Prog], mutation_rate: float) -> list[Prog]:
        pass

    def evolve_population(self, population: list[list[Prog]], fitness_scores: list[int], crossover_rate: float, mutation_rate: float) -> list[list[Prog]]:
        pass

    def optimize(self, time_matrix: list[int], passengers_demand: list[Demand]) -> list[Prog]:
        pass