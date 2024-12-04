"""
Fonctions utilitaires pour évaluer la qualité des horaires.
Calcule temps d'attente, violations de contraintes et métriques d'optimisation.
Fournit outils de visualisation et comparaison des solutions.
"""
from typing import List
import pandas as pd

from src.models.schedule import Schedule


class Evaluator:
    @staticmethod
    def calculate_objective(schedule: Schedule) -> float:
        """Calcule la fonction objectif pour un horaire"""
        pass

    @staticmethod
    def check_constraints(schedule: Schedule) -> List[str]:
        """Vérifie et retourne les violations de contraintes"""
        pass

    @staticmethod
    def compare_solutions(solutions: List[Schedule]) -> pd.DataFrame:
        """Compare différentes solutions selon plusieurs critères"""
        pass

    @staticmethod
    def visualize_schedule(schedule: Schedule):
        """Génère une visualisation de l'horaire"""
        pass