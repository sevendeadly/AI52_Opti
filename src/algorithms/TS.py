"""
Gilles NGASSAM & Daniel KOANGA
07/01/2025
"""

"""
Implémente l'Algorithme de Recherche Tabou pour l'optimisation des horaires de bus.
Utilise une mémoire tabou pour éviter les solutions déjà explorées et favorise la recherche d'optimums locaux et globaux.
Paramètres clés : taille de la liste tabou, critère d'arrêt, méthode de diversification.

Let's assume between midnigh and 6am, there is no bus
"""
# libraries importation
from src.models.plan import Prog, is_valid_plan, generate_derivated_plan, generate_random_plan, generate_plan_on_peak
from src.models.stations import process_global_waiting_time
from src.models.demand import Demand
from src.utils.time import DAYTIME
import random as rd
from copy import deepcopy

class TabuSearch:
    def __init__(
            self, 
            max_list_shape: int, 
            num_iterations: int, 
            num_progs: int, 
            num_locomotions: int,
            locomotion_capacity: int,
            time_matrix: list[int],
            passengers_demand: list[Demand],
            peak_repartition: list[(DAYTIME, float)],
            target_fitness=0.0,
        ):
        """
        Initialize the tabu search algorithm with the given parameters

        Args:
            max_list_shape (int): The length of a Tabu search list
            num_iterations (int): maximum number of iterations
            num_progs (int): Number of progs in the schedule
            num_locomotions (int): Number of locomotions in the schedule
            locomotion_capacity (int): Capacity of each locomotion
            time_matrix (list[int]): List of time intervals between each stop
            passengers_demand (list[Demand]): List of passengers demand
            peak_repartition (list[(DAYTIME, float)]): peak constraints with daytime intervals and associated probabilities
            target_fitness (float): The fitness targeted by the optimisation
        """
        self.max_list_shape = max_list_shape
        self.num_iterations = num_iterations
        self.target_fitness = target_fitness
        self.num_progs = num_progs
        self.num_locomotions = num_locomotions
        self.locomotion_capacity = locomotion_capacity
        self.time_matrix = time_matrix
        self.passengers_demand = passengers_demand
        self.peak_repartition = peak_repartition

    def evaluate_solution(self, plan: list[Prog]) -> int:
        return process_global_waiting_time(plan, self.passengers_demand*1, self.time_matrix, self.locomotion_capacity)
    
    def find_best_tabou_move(self, plan: list[Prog], index:int) -> tuple[int, int, bool]:
        neighbors: list[list[Prog]] = []
        tabou_moves = [
            (index, 2, False), (index, 1, False), (index, -1, False), (index, -2, False), 
            (index, 2, False), (index, 1, True), (index, 0, True), (index, -1, True), (index, -2, False)
        ]
        neighbor_costs: list[int] = []

        # Generate neighbor from tabou moves array
        for changer in tabou_moves:
            neighbors.append(generate_derivated_plan(plan, changer))

        for neighbor in neighbors:
            neighbor_costs.append(self.evaluate_solution(neighbor))

        best_neighbor_index = neighbor_costs.index(min(neighbor_costs))

        return tabou_moves[best_neighbor_index]
    
    def optimize(self):
        # Generate an initial solution, consider it as the best one
        best_plan = generate_plan_on_peak(self.num_progs, sum(self.time_matrix), self.peak_repartition)
        best_cost = self.evaluate_solution(best_plan)
        # Create an exploration best solution 
        exploration_best_plan = best_plan
        exploration_best_cost = best_cost
        # initialize the iterations and the tabou list
        current_iteration = 0
        tabou_list: list[tuple[int, int, bool]] = []

        print("best_cost : ", best_cost)
        
        # Set an algorithm's breaking condition
        while current_iteration < self.num_iterations or best_cost <= self.target_fitness:
            print("Iteration : ", current_iteration+1)
            local_best_plans: list[list[Prog]] = []
            local_tabou_moves: list[tuple[int, int, bool]] = []
            local_best_costs: list[int] = []

            for index, _ in enumerate(exploration_best_plan):
                local_tabou_move = self.find_best_tabou_move(exploration_best_plan, index)
                local_best_plan = generate_derivated_plan(exploration_best_plan, local_tabou_move)

                local_best_plans.append(local_best_plan)
                local_tabou_moves.append(local_tabou_move)
                local_best_costs.append(self.evaluate_solution(local_best_plan))

            local_best_costs = [int(cost) for cost in local_best_costs]
            print("tabou_list : ", tabou_list)

            if(min(local_best_costs) < best_cost):
                absolute_best_index = local_best_costs.index(min(local_best_costs))
                best_plan = local_best_plans[absolute_best_index]
                best_cost = min(local_best_costs)
                exploration_best_plan = local_best_plans[absolute_best_index]
                exploration_best_cost = best_cost

                tabou_list.insert(0, local_tabou_moves[absolute_best_index])
                tabou_list = tabou_list[:self.max_list_shape]
            else:
                current_index: int = local_best_costs.index(min(local_best_costs))
                local_best_cost = local_best_costs[current_index]
                local_tabou_move = local_tabou_moves[current_index]
                local_best_plan = local_best_plans[current_index]
                excluded_indexes: list[int] = []

                while(local_best_cost != min(
                        local_best_costs[idx] for idx in range(len(local_best_costs)) if idx not in excluded_indexes
                    ) or tabou_list.__contains__(local_tabou_move)
                ):
                    # Exclude the current index
                    excluded_indexes.append(current_index)
                    excluded_indexes = list(set(excluded_indexes))
                    print("Excluded indexes : ", excluded_indexes)

                    local_best_cost = min(
                        local_best_costs[idx] for idx in range(len(local_best_costs)) if idx not in excluded_indexes
                    )
                    indexes_list = [index for index, value in enumerate(local_best_costs) if value == local_best_cost and index not in excluded_indexes]
                    current_index = indexes_list[0]
                    local_tabou_move = local_tabou_moves[current_index]
                    local_best_plan = local_best_plans[current_index]

                tabou_list.insert(0, local_tabou_move)
                tabou_list = tabou_list[:self.max_list_shape]
                exploration_best_plan = local_best_plan
                exploration_best_cost = self.evaluate_solution(local_best_plan)

            print("Exploration cost : ", exploration_best_cost)
            # Update the global best stats
            if exploration_best_cost < best_cost:
                best_plan = exploration_best_plan
                best_cost = exploration_best_cost

            print("best cost : ", best_cost)
                
            current_iteration += 1
        
        return best_plan