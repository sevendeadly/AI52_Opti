#Author : Josue-Daniel

"""
Implémente le Recuit Simulé pour l'optimisation des horaires de bus.
Gère le schéma de refroidissement, la génération de voisins et la probabilité d'acceptation.
Paramètres clés : température initiale, taux de refroidissement, itérations par température
"""

# Librairies importation
import math
import random as rd
from src.models.plan import Prog
from src.models.plan import generate_derivated_plan, generate_random_plan
from src.models.demand import Demand
from src.models.stations import process_global_waiting_time

class SimulatedAnnealing:
    def __init__(
            self, 
            initial_temperature: float, 
            cooling_rate: float, 
            iterations_per_temperature: int, 
            temperature_threshold: float,
            num_progs: int,
            time_matrix: list[int],
            passengers_demand: list[Demand],
            num_locomotions: int,
            locomotion_capacity: int
        ):
        """
        Initialize the Simulated Annealing algorithm with the given parameters.

        Args:
            initial_temperature (float): initial temperature
            cooling_rate (float): cooling rate
            iterations_per_temperature (int): number of iterations per temperature
            temperature_threshold (float): temperature threshold
            num_progs (int): number of programs
            time_matrix (list[int]): list of time intervals between each stop
            passengers_demand (list[Demand]): list of passengers demand
            num_locomotions (int): number of locomotions in the schedule
            locomotion_capacity (int): capacity of each locomotion
        
        Returns:
            None
        """
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.iterations_per_temperature = iterations_per_temperature
        self.temperature_threshold = temperature_threshold
        self.num_progs = num_progs
        self.time_matrix = time_matrix
        self.passengers_demand = passengers_demand
        self.num_locomotions = num_locomotions
        self.locomotion_capacity = locomotion_capacity
        


    # Generate a neighbor solution
    def generate_neighbor(self, current_solution: list[Prog]) -> list[Prog]:
        """
        Generate a neighbor solution.

        Args:
            current_solution (list[Prog]): current solution

        Returns:
            list[Prog]: neighbor solution
        """
        return generate_derivated_plan(current_solution.copy())
    
    # Calculate the acceptance probability of a new solution
    def acceptance_probability(self, current_cost: int, new_cost: int, temperature: float) -> float:
        """
        Calculate the acceptance probability of a new solution.

        Args:
            current_cost (int): current cost
            new_cost (int): new cost
            temperature (float): current temperature

        Returns:
            float: acceptance probability
        """
        if new_cost < current_cost:
            return 1.0
        return math.exp((current_cost - new_cost) / temperature)
    
    def process_solution_fitness(self, solution: list[Prog]) -> int:
        """
        Process the fitness of a solution.

        Args:
            solution (list[Prog]): solution to evaluate

        Returns:
            int: fitness of the solution
        """
        return process_global_waiting_time(solution, self.passengers_demand*1, self.time_matrix, self.locomotion_capacity)
    
    # Run the Simulated Annealing algorithm
    def optimize(self) -> list[Prog]:
        """
        Run the Simulated Annealing algorithm.

        Returns:
            list[Prog]: optimized solution
        """
        # Initialize the current solution
        current_solution = generate_random_plan(self.num_progs, sum(self.time_matrix))
        current_cost = self.process_solution_fitness(current_solution)

        # Initialize the best solution
        best_solution = current_solution
        best_cost = current_cost

        # Initialize the temperature
        temperature = self.initial_temperature

        # Run the algorithm
        while temperature > self.temperature_threshold:
            print("Temperature : ", temperature)
            for _ in range(self.iterations_per_temperature):
                # Generate a neighbor solution
                new_solution = self.generate_neighbor(current_solution*1)
                new_cost = self.process_solution_fitness(new_solution)

                # Calculate the acceptance probability
                probability = self.acceptance_probability(current_cost, new_cost, temperature)

                # Accept the new solution
                if probability > rd.random():
                    current_solution = new_solution
                    current_cost = new_cost
                    print("New local best solution found : ", current_cost)

                # Update the best solution
                if current_cost < best_cost:
                    print("New global best solution found : ", current_cost)
                    best_solution = current_solution
                    best_cost = current_cost

            # Cool down the temperature
            temperature *= 1 - self.cooling_rate

        return best_solution