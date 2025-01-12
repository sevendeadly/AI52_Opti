"""
Gilles NGASSAM & Daniel KOANGA
09/01/2025
"""

# libraries importation
from abc import ABC, abstractmethod
from src.models.plan import Prog

class Optimizer(ABC):

    # Abstract method to optimize the plan
    @abstractmethod
    def optimize(self) -> tuple[list[Prog], list[float]]:
        pass