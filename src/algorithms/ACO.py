"""
Gilles NGASSAM & Daniel KOANGA
09/01/2025
"""

"""
Implements Ant Colony Optimization for locomotion schedules.
Manages pheromone trails and ant movement decisions.
Key parameters: number of ants, evaporation rate, visibility factor, pheromone factor

Let's assume between midnight and 6am, there is no locomotions
"""

# libraries importation
from src.algorithms.Optimizer import Optimizer
from src.algorithms.Logger import Logger
from src.models.plan import Prog, is_valid_plan
from src.models.stations import process_global_waiting_time
from src.models.demand import Demand
from src.utils.constants import SERVICE_START, SERVICE_END, NUM_PROGS, DIRECTION_REPARTITION
from src.utils.time import convertTimeStamp
import random as rd
from collections import Counter
import numpy as np

class AntColonyOptimization(Optimizer, Logger):
    def __init__(
            self, 
            num_ants: int, 
            num_iterations: int, 
            alpha: float, 
            beta: float, 
            rho: float, 
            passenger_demands: list[Demand], 
            time_matrix: list[int]
        ):
        """
        ACO class constructor

        Args:
            num_ants (int): number of ants in the colony
            num_iterations (int): maximum number of iterations
            alpha (float): pheromone factor
            beta (float): visibility factor
            rho (float): evaporation rate
            passenger_demands (list[Demand]): list of passengers demand
            time_matrix (list[int]): list of time intervals between each stop

        Returns:
            None
        """
        super().__init__(num_iterations)
        self.num_ants = num_ants
        self.num_iterations = num_iterations
        self.evaporation_rate = rho
        self.visibility_factor = beta
        self.pheromone_factor = alpha
        self.passenger_demands = passenger_demands
        self.time_matrix = time_matrix
        
        # Initialize pheromone and visibility trails
        self.pheromone_trails: list[list[float]] = np.ones((2, SERVICE_END - SERVICE_START))
        self.visibility_trails: list[list[float]] = np.zeros((2, SERVICE_END - SERVICE_START))
        self.process_visibility_trail()

    # Process the visibility trails
    def process_visibility_trail(self):
        """
        Process the visibility trails
        
        Returns:
            None
        """
        for i in range(len(self.visibility_trails)):
            direction = False if i == 0 else True

            for j in range(len(self.visibility_trails[i])):
                # derive and estimate the waiting time for each time slot in both directions
                time = convertTimeStamp((j + SERVICE_START) * 60)
                prog = Prog(time, sum(self.time_matrix), direction)
                waiting_time = self.evaluate_solution([prog])

                # Update the visibility trail by inversing the waiting time
                self.visibility_trails[i][j] = (1 / (waiting_time*60*60*self.passenger_demands.__len__()))

    # Evaluate the fitness of a locomotion plan
    def evaluate_solution(self, plan: list[Prog]) -> float:
        """
        Evaluate the fitness of a locomotion plan

        Args:
            plan (list[Prog]): the plan to evaluate

        Returns:
            int: the fitness of the plan
        """
        global_waiting_time = process_global_waiting_time(plan, self.passenger_demands*1, self.time_matrix) 
        global_waiting_time /= (60*60*self.passenger_demands.__len__())
        
        return round(global_waiting_time , 5)    

    # Update pheromone trails by ant movement
    def update_pheromone_trails(self, ant_plans: list[list[Prog]]):
        """
        Update pheromone trails by ant movement

        Args:
            ant_plans (list[list[Prog]]): list of ant plans
        """
        # Evaporate the pheromone trails
        for i in range(self.pheromone_trails.__len__()):
                for j in range(self.pheromone_trails[i].__len__()):
                    self.pheromone_trails[i][j] *= (1 - self.evaporation_rate)

        # Add the pheromone generated by the ants recent movements 
        for ant_plan in ant_plans:
            plan_waiting_time = self.evaluate_solution(ant_plan)*60*60*self.passenger_demands.__len__()
            for i in range(len(ant_plan)):
                position = (ant_plan[i].time.hour * 60 + ant_plan[i].time.minute) - SERVICE_START
                direction = 1 if ant_plan[i].direction else 0
                
                self.pheromone_trails[direction][position] += (1 / plan_waiting_time)

    # Optimize the locomotion plan using Ant Colony Optimization
    def optimize(self) -> tuple[list[Prog], list[float]]:
        """
        Optimize the locomotion plan using Ant Colony Optimization

        Returns:
            tuple[list[Prog], list[float]]: the best plan and the fitness evolution
        """
        # Save metrics for fitness evolution
        fitness_evolution: list[float] = []
        best_plan = None
        best_fitness = float('inf')
        for _ in range(self.num_iterations):
            ant_plans: list[list[Prog]] = []
            # Take into account pheromone trails and visibility before initializing ants
            for _ in range(self.num_ants):
                ant_plan: list[Prog] = []
                all_progs_directions = rd.choices([False, True], weights=DIRECTION_REPARTITION, k=NUM_PROGS)

                while not is_valid_plan(ant_plan) or ant_plan.__len__() != NUM_PROGS:
                    ant_plan: list[Prog] = []

                    # Choose the next time slot based on pheromone trails and visibility on the down direction
                    probabilities = [
                        (self.pheromone_trails[0][pos - SERVICE_START] ** self.pheromone_factor) *
                        (self.visibility_trails[0][pos - SERVICE_START] ** self.visibility_factor)
                        for pos in range(SERVICE_START, SERVICE_END)
                    ]
                    total = sum(probabilities)
                    probabilities = [prob / total for prob in probabilities]
                    positions = rd.choices(range(SERVICE_START, SERVICE_END), weights=probabilities, k=Counter(all_progs_directions)[False])

                    for position in positions:
                        direction = False
                        time = convertTimeStamp(position*60)

                        prog = Prog(time, sum(self.time_matrix), direction)
                        ant_plan.append(prog)
                    
                    # Choose the next time slot based on pheromone trails and visibility on the up direction
                    probabilities = [
                        (self.pheromone_trails[1][pos - SERVICE_START] ** self.pheromone_factor) *
                        (self.visibility_trails[1][pos - SERVICE_START] ** self.visibility_factor)
                        for pos in range(SERVICE_START, SERVICE_END)
                    ]
                    total = sum(probabilities)
                    probabilities = [prob / total for prob in probabilities]
                    positions = rd.choices(range(SERVICE_START, SERVICE_END), weights=probabilities, k=Counter(all_progs_directions)[True])

                    for position in positions:
                        direction = True
                        time = convertTimeStamp(position*60)

                        prog = Prog(time, sum(self.time_matrix), direction)
                        ant_plan.append(prog)

                # Sort the plan by time before adding it to the list of ant plans
                ant_plan.sort(key=lambda prog: prog.time)
                ant_plans.append(ant_plan)

            # Evaluate fitness of each ant
            fitnesses = [self.evaluate_solution(ant_plan) for ant_plan in ant_plans]

            # Update best plan
            min_fitness = min(fitnesses)
            # Track the best metrics
            fitness_evolution.append(min_fitness)

            if min_fitness < best_fitness:
                best_fitness = min_fitness
                best_plan = ant_plans[fitnesses.index(min_fitness)]

            # Update pheromone trails by evaporation and movements
            self.update_pheromone_trails(ant_plans*1)

            # Update the loader
            self.update(best_fitness)

        return best_plan, fitness_evolution