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
import random as rd
from src.utils.time import convertTimeStamp
from src.models.stations import process_global_waiting_time
from src.utils.constants import MAX_LOCOMOTION_SLOT_VARIATION

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
            selection_rate: float,
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
            selection_rate (float): Probability of selection
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
        self.selection_rate = selection_rate
        self.num_slots = num_slots
        self.num_locomotions = num_locomotions
        self.locomotion_capacity = locomotion_capacity
        self.time_matrix = time_matrix
        self.passengers_demand = passengers_demand
        self.initial_population = self.generate_population()

    # Generate a random individual
    def generate_individual(self) -> list[Prog]:
        """
        Generate a random individual
        
        Returns:
            list[Prog]: a random individual with a proposed schedule
        """
        individual: list[Prog] = []

        while not self.is_valid_individual(individual):
            # Initialize an empty individual
            individual: list[Prog] = []

            for _ in range(self.num_slots):
                # Generate a random time 
                    # SERVICE_START * 60) + 1 : Served at least 1 second after the start of the service
                    # SERVICE_END * 60) - 1 : Served at least 1 second before the end of the service
                start_time_seconds = int(rd.randint((SERVICE_START * 60) + 1, (SERVICE_END * 60) - 1)) 
                start_time_seconds -= start_time_seconds % 60 # round to the nearest minute
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
        """
        Check if an individual is valid according to the constraints

        Args:
            individual (list[Prog]): the individual to check

        Returns:
            bool: True if the individual is valid, False otherwise
        """
        return is_valid_plan(individual, self.num_locomotions) and individual.__len__() <= self.num_slots and individual.__len__() > 0
    
    # Generate the initial population
    def generate_population(self) -> list[list[Prog]]:
        """
        Generate the initial population
        
        Returns:
            list[list[Prog]]: the initial population
        """
        population: list[list[Prog]] = []

        for _ in range(self.population_size):
            individual = self.generate_individual()
            population.append(individual)

        return population

    # Evaluate the fitness of the population
    def evaluate_individual(self, individual: list[Prog]) -> int:
        """
        Evaluate the fitness of an individual

        Args:
            individual (list[Prog]): the individual to evaluate

        Returns:
            int: the fitness score of the individual
        """
        return process_global_waiting_time(individual, self.passengers_demand, self.time_matrix, self.locomotion_capacity)

    # Select the parents of the next generation according to their fitness (elite selection)
    def select_parents(self) -> list[list[Prog]]:
        """
        Select the parents of the next generation according to their fitness (elite selection)
        
        Returns:
            list[list[Prog]]: the elite population
        """
        ranked_population = self.initial_population.copy()
        ranked_population.sort(key=lambda individual: self.evaluate_individual(individual))

        # Select the elite individuals according to the crossover rate
        num_elite = int((self.population_size * self.selection_rate) + 1) # round up to the next integer
        elite_parents = ranked_population[:num_elite]

        return elite_parents

    # Perform the crossover operation
    def crossover(self, parent1: list[Prog], parent2: list[Prog]) -> list[list[Prog]]:
        """
        Perform the crossover operation

        Args:
            parent1 (list[Prog]): the first parent
            parent2 (list[Prog]): the second parent

        Returns:
            list[list[Prog]]: the children resulting from the crossover
        """
        if rd.random() < self.crossover_rate:
            children: list[list[Prog]] = []

            while children.__len__() < 2:
                # Select a random crossover point
                crossover_point = rd.randint(1, self.num_slots - 1)

                # Perform the crossover and check the validity of the children
                child1 = parent1[:crossover_point] + parent2[crossover_point:]
                child2 = parent2[:crossover_point] + parent1[crossover_point:]

                if self.is_valid_individual(child1):
                    children.append(child1)

                if self.is_valid_individual(child2):
                    children.append(child2)
            
            return children
        else:
            return [parent1, parent2]

    # Perform the mutation operation
    def mutate(self, individual: list[Prog]) -> list[Prog]:
        if rd.random() < self.mutation_rate:
            mutated_individual = individual.copy()

            # Select a random mutation point
            prog_to_mutate = rd.choice(mutated_individual)
            mutated_individual.remove(prog_to_mutate)

            # Get the start time of the prog to mutate
            prog_to_mutate_start_time = prog_to_mutate.process_tour_start()

            while not self.is_valid_individual(mutated_individual):
                # Generate a random time variation
                random_time_seconds = int(rd.randint(-MAX_LOCOMOTION_SLOT_VARIATION, MAX_LOCOMOTION_SLOT_VARIATION) * 60)
                new_start_time_seconds = prog_to_mutate_start_time + random_time_seconds
                # Make sure the departure time is within the service hours
                new_start_time_seconds = max(new_start_time_seconds, SERVICE_START * 60)
                new_start_time_seconds = min(new_start_time_seconds, SERVICE_END * 60)
                new_start_time = convertTimeStamp(new_start_time_seconds)

                # Try to add it to the mutated
                new_prog = Prog(new_start_time, prog_to_mutate.duration, prog_to_mutate.direction)
                if self.is_valid_individual(mutated_individual + [new_prog]):
                    mutated_individual.append(new_prog)

            # sort the mutated individual by time
            mutated_individual.sort(key=lambda prog: prog.time)

            return mutated_individual
        
        return individual

    # Evolve the population
    def evolve_population(self) -> list[list[Prog]]:
        """
        Evolve the population

        Returns:
            list[list[Prog]]: the new population
        """
        # Select the best parents
        elite_parents = self.select_parents()

        # Generate the children
        children: list[list[Prog]] = []
        while children.__len__() < self.population_size:
            parents = rd.choices(elite_parents, k=2)

            children += self.crossover(parents[0], parents[1])

        # Mutate the children
        mutated_children = [self.mutate(child) for child in children]

        # Create the new population
        new_population = elite_parents + mutated_children
        new_population.sort(key=lambda individual: self.evaluate_individual(individual))

        return new_population[:self.population_size]

    # Optimize the transportation plan
    def optimize(self) -> list[Prog]:
        """
        Optimize the transportation plan by running the genetic algorithm for the given number of generations

        Returns:
            list[Prog]: the optimized transportation plan
        """
        current_population = self.initial_population.copy()

        # run through all the generations
        for iteration in range(self.num_generations):
            print(f"Generation {iteration + 1} / {self.num_generations}")
            self.initial_population = current_population
            current_population = self.evolve_population()

        return min(current_population, key=lambda individual: self.evaluate_individual(individual))