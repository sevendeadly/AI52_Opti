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
from src.models.plan import Prog, is_valid_plan, generate_derivated_plan, generate_random_plan, generate_plan_on_peak
from src.models.demand import Demand
import random as rd
from src.models.stations import process_global_waiting_time
from src.utils.time import DAYTIME

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
            passengers_demand: list[Demand],
            peak_repartition: list[(DAYTIME, float)]
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
            peak_repartition (list[(DAYTIME, float)]): peak constraints with daytime intervals and associated probabilities

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
        self.peak_repartition = peak_repartition
        self.initial_population = self.generate_population()
        

    # Generate a random individual
    def generate_individual(self) -> list[Prog]:
        """
        Generate a random individual
        
        Returns:
            list[Prog]: a random individual with a proposed schedule
        """
        individual = generate_plan_on_peak(self.num_slots, sum(self.time_matrix), self.peak_repartition)

        while not self.is_valid_individual(individual):
            individual = generate_plan_on_peak(self.num_slots, sum(self.time_matrix), self.peak_repartition)

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
        return is_valid_plan(individual, self.num_locomotions) and individual.__len__() <= self.num_slots
    
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
        global_waiting_time = process_global_waiting_time(individual, self.passengers_demand*1, self.time_matrix, self.locomotion_capacity)
        return round(global_waiting_time / (60*60*self.passengers_demand.__len__()), 2)

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
            return generate_derivated_plan(individual)
        
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

        print("Best individual : ", self.evaluate_individual(new_population[0]))
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