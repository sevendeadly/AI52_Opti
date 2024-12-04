# AI52_public-transport-metaheuristics
Optimisation des horaires de transport public utilisant divers algorithmes métaheuristiques (Recuit Simulé, Algorithme Génétique, Recherche Tabou, Optimisation par Colonies de Fourmis, Optimisation par Essaim Particulaire).

## Aperçu du Projet
Implémentation d'algorithmes métaheuristiques pour optimiser les horaires des bus publics. L'objectif est de minimiser les temps d'attente des passagers tout en respectant les contraintes de disponibilité des véhicules.

### Description du Problème
- Optimiser les horaires des bus sur plusieurs arrêts
- Minimiser le temps d'attente global des passagers
- Gérer plusieurs itinéraires par véhicule
- Tenir compte des contraintes de maintenance et de temps de transit
- Respecter les heures d'exploitation pour chaque arrêt

## Algorithmes
Implémentation et comparaison de 5 approches métaheuristiques :
1. Recuit Simulé (SA)
2. Algorithme Génétique (GA)
3. Recherche Tabou (TS)
4. Optimisation par Colonies de Fourmis (ACO)
5. Optimisation par Essaim Particulaire (PSO)

## Structure du Projet
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


## Prérequis du Projet
- Python 3.8+
- NumPy
- Pandas
- Matplotlib
- Jupyter (pour la visualisation des résultats)


## Installation
```bash
git clone https://github.com/yourusername/public-transport-metaheuristics.git
cd public-transport-metaheuristics
pip install -r requirements.txt
```

## Utilisation
```python
from src.algorithms import SimulatedAnnealing, GeneticAlgorithm
from src.models import Schedule

# Charger l'instance du problème
schedule = Schedule.from_json('data/sample_instance.json')

# Exécuter l'optimisation
sa_solution = SimulatedAnnealing(schedule).optimize()
ga_solution = GeneticAlgorithm(schedule).optimize()
```
