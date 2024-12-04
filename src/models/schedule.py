"""
Structure de données principale pour la représentation des horaires.
Gère la validation, vérification des contraintes et calcul des objectifs.
Inclut méthodes de manipulation et d'évaluation des horaires.
"""
from typing import List, Dict


class BusStop:
    def __init__(self, id: int, name: str, demand: Dict[str, int]):
        self.id = id
        self.name = name
        self.demand = demand  # demande par période

class Bus:
    def __init__(self, id: int, capacity: int):
        self.id = id
        self.capacity = capacity
        self.schedule = []

class Schedule:
    def __init__(self, buses: List[Bus], stops: List[BusStop]):
        self.buses = buses
        self.stops = stops

    def calculate_waiting_time(self) -> float:
        """Calcule le temps d'attente total"""
        pass

    def is_valid(self) -> bool:
        """Vérifie si l'horaire respecte toutes les contraintes"""
        pass

    def serialize(self) -> Dict:
        """Convertit l'horaire en format JSON"""
        pass

    @classmethod
    def deserialize(cls, data: Dict) -> 'Schedule':
        """Crée un horaire à partir d'un format JSON"""
        pass