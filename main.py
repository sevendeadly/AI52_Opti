from src.models.stations import generate_time_matrix, process_global_waiting_time
from src.models.demand import generate_demand_sample, save_demand_as_instance, load_demand_from_instance
from src.models.plan import process_required_locomotions, save_plan_csv
from src.utils.constants import NUM_STOPS, PEAK_REPARTITION, PASSENGERS_DEMAND, TIME_MATRIX
from src.algorithms.TS import TabuSearch
from src.algorithms.ACO import AntColonyOptimization
from src.algorithms.PSO import ParticleSwarmOptimization
from src.algorithms.GA import GeneticAlgorithm
from src.algorithms.SA import SimulatedAnnealing
from src.algorithms.Optimizer import Optimizer
import matplotlib.pyplot as plt

def visualization(fitness_variations: list[float]):
    """
    Visualization of the evolution of the cost of the solution

    Args:
        fitness_variations (list[float]): list of fitness variations
    
    """
    data_in_minutes = [fitness*60 for fitness in fitness_variations]
    plt.plot(data_in_minutes)
    plt.title('Average waiting time along the iterations')
    plt.xlabel('Iterations evolution') 
    plt.ylabel('Average waiting time (minutes)')

    # Adding indices on the graph
    worst_fitness = max(data_in_minutes)
    worst_generation = data_in_minutes.index(worst_fitness)
    plt.text(worst_generation, worst_fitness, "worst fitness", fontsize=6, ha='left', va='bottom')

    best_fitness = min(data_in_minutes)
    best_generation = data_in_minutes.index(best_fitness)
    plt.text(best_generation, best_fitness, "best fitness", fontsize=6, ha='left', va='bottom')

    plt.show()



if __name__ == '__main__':
    time_matrix = TIME_MATRIX # generate_time_matrix(NUM_STOPS)

    # demands = generate_demand_sample(time_matrix.__len__() + 1, PASSENGERS_DEMAND, PEAK_REPARTITION)

    # save_demand_as_instance(demands, 'instance_5')

    demands = load_demand_from_instance('instance_3')

    chosen_heuristic: Optimizer = None
    ts = TabuSearch(8, 100, demands, time_matrix, 0.05)
    # ga = GeneticAlgorithm(100, 15, 0.7, 0.1, 0.8, passengers_demand=demands*1, time_matrix=time_matrix)
    # sa = SimulatedAnnealing(170000, 0.05, 50, 1000, demands*1, time_matrix)
    # aco = AntColonyOptimization(20, 100, 3, 1, 0.1, demands*1, time_matrix)
    # pso = ParticleSwarmOptimization(30, 100, 0.6, 1.5, 1, demands*1, time_matrix)

    # select the heuristic to use
    chosen_heuristic = ts

    # Start the optimization process
    print("\rTabu Search Algorithm.")
    best_solution, historic = chosen_heuristic.optimize()


    # visualization(historic)
    visualization(historic)

    # Display the results of the optimization
    mean_waiting_time = process_global_waiting_time(best_solution, demands, time_matrix) / demands.__len__()
    hours, minutes, seconds = int(mean_waiting_time // 3600), int((mean_waiting_time % 3600) // 60), int(mean_waiting_time % 60)

    print(f"\rThe average waiting time is estimated to {hours} hours {minutes} minutes and {seconds} seconds.")

    num_journeys = best_solution.__len__()
    used_locomotions = process_required_locomotions(best_solution).__len__()
    print(f"\rIt takes {num_journeys} journeys satisfied by {used_locomotions} vehicles.")

    # Display the plan generated
    best_solution.sort(key=lambda prog: prog.direction)
    for prog in best_solution:
        print(prog)
    
    # Save the plan generated
    save_plan_csv(best_solution, 'plan')
    print("\rThe proposed plan has been saved at 'data/output/plan.csv'")