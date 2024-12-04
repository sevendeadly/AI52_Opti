# AI52_public-transport-metaheuristics

Optimization of public transport schedules using various metaheuristic algorithms (Simulated Annealing, Genetic Algorithm, Tabu Search, Ant Colony Optimization, Particle Swarm Optimization).

## Project Overview

Implementation of metaheuristic algorithms to optimize public bus transport schedules. The goal is to minimize passenger waiting times while respecting vehicle availability constraints.

### Problem Description

- Optimize bus schedules across multiple stops
- Minimize overall passenger waiting time
- Handle multiple routes per vehicle
- Consider maintenance and transit time constraints
- Respect operating hours for each stop

## Algorithms

Implementation and comparison of 5 metaheuristic approaches:

1. Simulated Annealing (SA)
2. Genetic Algorithm (GA)
3. Tabu Search (TS)
4. Ant Colony Optimization (ACO)
5. Particle Swarm Optimization (PSO)

## Project Structure

```
public-transport-metaheuristics/
├── src/
│   ├── algorithms/
│   │   ├── simulated_annealing.py
│   │   ├── genetic_algorithm.py
│   │   ├── tabu_search.py
│   │   ├── ant_colony.py
│   │   └── particle_swarm.py
│   ├── models/
│   │   └── schedule.py
│   └── utils/
│       └── evaluation.py
├── data/
│   └── sample_instance.json
├── tests/
├── docs/
│   └── mathematical_model.md
└── results/
    └── comparison.ipynb
```

## Installation

```bash
git clone https://github.com/yourusername/public-transport-metaheuristics.git
cd public-transport-metaheuristics
pip install -r requirements.txt
```

## Usage

```python
from src.algorithms import SimulatedAnnealing, GeneticAlgorithm
from src.models import Schedule

# Load problem instance
schedule = Schedule.from_json('data/sample_instance.json')

# Run optimization
sa_solution = SimulatedAnnealing(schedule).optimize()
ga_solution = GeneticAlgorithm(schedule).optimize()
```

## Project Requirements

- Python 3.8+
- NumPy
- Pandas
- Matplotlib
- Jupyter (for results visualization)


## License

MIT License
