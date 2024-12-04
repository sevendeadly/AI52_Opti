import argparse
""" 
from src.algorithms import (
    SimulatedAnnealing,
    GeneticAlgorithm,
    TabuSearch,
    AntColony,
    ParticleSwarm
)
"""

from src.models.schedule import Schedule
from src.utils.evaluation import Evaluator
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(description='Public Transport Schedule Optimization')
    parser.add_argument('--algorithm', type=str, default='all',
                        choices=['sa', 'ga', 'ts', 'aco', 'pso', 'all'],
                        help='Metaheuristic algorithm to use')
    parser.add_argument('--data', type=str, default='data/sample_instance.json',
                        help='Path to problem instance')
    parser.add_argument('--output', type=str, default='results/comparison.json',
                        help='Output file path')
    return parser.parse_args()


def main():
    args = parse_args()
    schedule = Schedule.from_json(args.data)

    algorithms = {
        'sa': SimulatedAnnealing,
        'ga': GeneticAlgorithm,
        'ts': TabuSearch,
        'aco': AntColony,
        'pso': ParticleSwarm
    }

    results = {}

    if args.algorithm == 'all':
        for name, algo in algorithms.items():
            logger.info(f"Running {name.upper()} optimization")
            optimizer = algo(schedule)
            results[name] = optimizer.optimize()
    else:
        optimizer = algorithms[args.algorithm](schedule)
        results[args.algorithm] = optimizer.optimize()

    #Evaluator.evaluate_results(results, args.output)


if __name__ == "__main__":
    main()