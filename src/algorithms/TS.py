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
from src.algorithms.Optimizer import Optimizer
from src.models.plan import Prog, generate_derivated_plan, generate_plan_on_peak
from src.models.stations import process_global_waiting_time
from src.models.demand import Demand
from src.utils.constants import NUM_PROGS, PEAK_REPARTITION

class TabuSearch(Optimizer):
    def __init__(
            self, 
            max_list_shape: int, 
            num_iterations: int, 
            passengers_demand: list[Demand],
            time_matrix: list[int],
            target_fitness=0.0,
        ):
        """
        Initialize the tabu search algorithm with the given parameters

        Args:
            max_list_shape (int): The length of a Tabu search list
            num_iterations (int): maximum number of iterations
            passengers_demand (list[Demand]): List of passengers demand
            time_matrix (list[int]): List of time intervals between each stop
            target_fitness (float): The fitness targeted by the optimisation
        """
        self.max_list_shape = max_list_shape
        self.num_iterations = num_iterations
        self.target_fitness = target_fitness
        self.time_matrix = time_matrix
        self.passengers_demand = passengers_demand

    def evaluate_solution(self, plan: list[Prog]) -> float:
        """
        Evaluate the solution cost

        Args:
            plan (list[Prog]): The plan to evaluate

        Returns:
            float: The cost of the plan
        """
        global_waiting_time: float = process_global_waiting_time(plan, self.passengers_demand*1, self.time_matrix)
        global_waiting_time /= (60*60*self.passengers_demand.__len__())

        return round(global_waiting_time, 5) 
    
    def find_best_tabou_move(self, plan: list[Prog], index:int) -> tuple[int, int, bool]:
        """
        Find the best tabou move for a given plan

        Args:
            plan (list[Prog]): The plan to evaluate
            index (int): The index of the plan to evaluate
        
        Returns:
            tuple[int, int, bool]: The best tabou move
        """
        neighbors: list[list[Prog]] = []
        tabou_moves = [
            (index, 2, False), (index, 1, False), (index, -1, False), (index, -2, False), 
            (index, 2, False), (index, 1, True), (index, 0, True), (index, -1, True), (index, -2, False)
        ]
        neighbor_costs: list[float] = []

        # Generate neighbor from tabou moves array
        for changer in tabou_moves:
            neighbors.append(generate_derivated_plan(plan, changer))

        for neighbor in neighbors:
            neighbor_costs.append(self.evaluate_solution(neighbor))

        best_neighbor_index = neighbor_costs.index(min(neighbor_costs))

        return tabou_moves[best_neighbor_index]
    
    def optimize(self):
        # Generate an initial solution, consider it as the best one
        best_plan = generate_plan_on_peak(NUM_PROGS, sum(self.time_matrix), PEAK_REPARTITION)
        best_cost: float = self.evaluate_solution(best_plan)
        # Create an exploration best solution 
        exploration_best_plan = best_plan
        exploration_best_cost = best_cost
        # initialize the iterations and the tabou list
        current_iteration = 0
        tabou_list: list[tuple[int, int, bool]] = []

        print("best_cost : ", best_cost)
        
        # Set an algorithm's breaking condition
        while current_iteration < self.num_iterations or best_cost <= self.target_fitness:
            print("Iteration : ", current_iteration+1, " / ", self.num_iterations)
            local_best_plans: list[list[Prog]] = []
            local_tabou_moves: list[tuple[int, int, bool]] = []
            local_best_costs: list[float] = []

            for index, _ in enumerate(exploration_best_plan):
                local_tabou_move = self.find_best_tabou_move(exploration_best_plan, index)
                local_best_plan = generate_derivated_plan(exploration_best_plan, local_tabou_move)

                local_best_plans.append(local_best_plan)
                local_tabou_moves.append(local_tabou_move)
                local_best_costs.append(self.evaluate_solution(local_best_plan))

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

            # Update the global best stats
            if exploration_best_cost < best_cost:
                best_plan = exploration_best_plan
                best_cost = exploration_best_cost

            print("best cost : ", best_cost)
                
            current_iteration += 1
        
        return best_plan