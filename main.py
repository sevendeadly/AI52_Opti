from src.models.stations import generate_time_matrix, process_global_waiting_time
from src.models.demand import generate_demand_sample, save_demand_as_instance, load_demand_from_instance
from src.models.plan import process_required_locomotions
from src.utils.constants import NUM_STOPS, PEAK_REPARTITION, PASSENGERS_DEMAND
from src.algorithms.TS import TabuSearch
from src.algorithms.ACO import AntColonyOptimization
from src.algorithms.PSO import ParticleSwarmOptimization
from src.algorithms.AG import GeneticAlgorithm
from src.algorithms.SA import SimulatedAnnealing
from src.algorithms.Optimizer import Optimizer

if __name__ == '__main__':
    time_matrix = generate_time_matrix(NUM_STOPS)

    # demands = generate_demand_sample(time_matrix.__len__() + 1, PASSENGERS_DEMAND, PEAK_REPARTITION)

    # save_demand_as_instance(demands, 'instance_1')

    demands = load_demand_from_instance('instance_1')

    chosen_heuristic: Optimizer = None
    # ts = TabuSearch(8, 100, demands, time_matrix, 3600)
    ga = GeneticAlgorithm(100, 10, 0.7, 0.1, 0.8, passengers_demand=demands*1, time_matrix=time_matrix)
    # sa = SimulatedAnnealing(10000, 0.05, 50, 1000, demands*1, time_matrix)
    # aco = AntColonyOptimization(20, 100, 1, 1, 0.1, demands*1, time_matrix)
    # pso = ParticleSwarmOptimization(100, 100, 0.6, 1.5, 1, demands*1, time_matrix)

    # select the heuristic to use
    chosen_heuristic = ga

    # Start the optimization process
    best_solution = chosen_heuristic.optimize()

    print("Best solution : ")
    best_solution.sort(key=lambda prog: prog.direction)
    for prog in best_solution:
        print(prog)

    # save_plan_csv(best_solution, 'plan')
    print("Global waiting time : ", process_global_waiting_time(best_solution, demands, time_matrix))
    print("Proposed slots : ", best_solution.__len__())
    print("Locomotions needed :  ", process_required_locomotions(best_solution).__len__())