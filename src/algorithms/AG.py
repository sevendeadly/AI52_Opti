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
from src.algorithms.Optimizer import Optimizer
from src.models.plan import Prog, is_valid_plan, generate_derivated_plan, generate_plan_on_peak
from src.utils.constants import PEAK_REPARTITION, NUM_PROGS
from src.models.demand import Demand
import random as rd
from src.models.stations import process_global_waiting_time


class GeneticAlgorithm(Optimizer):
    # Constructor
    def __init__(
            self, num_generations: int, 
            population_size: int, 
            crossover_rate: float, 
            mutation_rate: float,
            selection_rate: float,
            passengers_demand: list[Demand],
            time_matrix: list[int],
        ):
        """
        Initialize the Genetic Algorithm with the given parameters

        Args:
            num_generations (int): Number of generations
            population_size (int): Number of individuals in the population
            crossover_rate (float): Probability of crossover
            mutation_rate (float): Probability of mutation
            selection_rate (float): Probability of selection
            passengers_demand (list[Demand]): List of passengers demand
            time_matrix (list[int]): List of time intervals between each stop

        Returns:
            None
        """
        self.num_generations = num_generations
        self.population_size = population_size
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.selection_rate = selection_rate
        self.time_matrix = time_matrix
        self.passengers_demand = passengers_demand
        

    # Generate a random individual
    def generate_individual(self) -> list[Prog]:
        """
        Generate a random individual
        
        Returns:
            list[Prog]: a random individual with a proposed schedule
        """
        individual = generate_plan_on_peak(NUM_PROGS, sum(self.time_matrix), PEAK_REPARTITION)

        while not self.is_valid_individual(individual):
            individual = generate_plan_on_peak(NUM_PROGS, sum(self.time_matrix), PEAK_REPARTITION)

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
        return is_valid_plan(individual) and individual.__len__() <= NUM_PROGS
    
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
        global_waiting_time = process_global_waiting_time(individual, self.passengers_demand*1, self.time_matrix)
        
        return round(global_waiting_time / (60*60*self.passengers_demand.__len__()), 5)

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
                # Select three random crossover points
                first_crossover_point = rd.randint(0, NUM_PROGS - 1)
                second_crossover_point = rd.randint(first_crossover_point, NUM_PROGS - 1)
                third_crossover_point = rd.randint(second_crossover_point, NUM_PROGS - 1)

                # Perform the crossover and check the validity of the children
                child1 = parent1[:first_crossover_point] + parent2[first_crossover_point:second_crossover_point] + parent1[second_crossover_point:third_crossover_point] + parent2[third_crossover_point:]
                child2 = parent2[:first_crossover_point] + parent1[first_crossover_point:second_crossover_point] + parent2[second_crossover_point:third_crossover_point] + parent1[third_crossover_point:]

                child1.sort(key=lambda prog: prog.time)
                child2.sort(key=lambda prog: prog.time)
                
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
            mutation_point = rd.randint(0, individual.__len__() - 1)
            minutes_rotation = rd.randint(-2,2)
            direction = rd.choice([True, False])
            changer = (mutation_point, minutes_rotation, direction)

            return generate_derivated_plan(individual, changer)
        
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
    def optimize(self) -> tuple[list[Prog], list[float]]:
        """
        Optimize the transportation plan by running the genetic algorithm for the given number of generations

        Returns:
            list[Prog]: the optimized transportation plan
        """
        # Save metrics for fitness evolution
        fitness_evolution: list[float] = []
        current_population = self.generate_population()

        # run through all the generations
        for iteration in range(self.num_generations):
            print(f"Generation {iteration + 1} / {self.num_generations}")
            self.initial_population = current_population
            current_population = self.evolve_population()
            # Track the best metrics
            fitness_evolution.append(self.evaluate_individual(current_population[0]))

        return min(current_population, key=lambda individual: self.evaluate_individual(individual)), fitness_evolution