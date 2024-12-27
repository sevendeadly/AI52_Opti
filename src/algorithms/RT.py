#Author : Josue-Daniel



"""
Implémente la Recherche Tabou pour l'optimisation des horaires de bus.
Maintient une liste taboue des mouvements récents et critères d'aspiration.
Paramètres clés : taille liste taboue, structure de voisinage, conditions d'aspiration
"""
import logging
from typing import List, Dict, Any, Tuple

from networkx.classes import neighbors

from src.models.schedule import *
import random
import copy

logger = logging.getLogger(__name__)


class TabuSearch:
    def __init__(self, initial_solution: Schedule, tabu_size:int=4, max_iterations:int=100):

        self.tabu_list = []
        self.initial_solution = initial_solution
        self.tabu_size = tabu_size
        self.max_iterations = max_iterations
        self.best_solution = None
        self.best_fitness = float('inf')
        self.non_improving_count = 0
        self.max_non_improving = 20  # Allow some non-improving moves before stopping

    def get_neighborhood(self, solution:Schedule) -> List[Tuple[Schedule, str]]:
        """Génère les voisins d'une solution"""
        neighbors = []

        #Echange horaire entre deux bus
        for i in range(len(solution.buses)):
            for j in range(i+1, len(solution.buses)):
                new_solution = copy.deepcopy(solution)
                bus1_sched = new_solution.buses[i].schedule
                new_solution.buses[i].schedule = new_solution.buses[j].schedule
                new_solution.buses[j].schedule = bus1_sched
                move_key = f"swap_buses_{i}_{j}"
                neighbors.append((new_solution, move_key))

        #Modifier ordre des arrêts ^pur un bus
        for i, bus in enumerate(solution.buses):
            if len(bus.schedule) >= 2:
                for j in range(len(bus.schedule) - 1):
                    new_solution = copy.deepcopy(solution)
                    sched = new_solution.buses[i].schedule
                    sched[j], sched[j+1] = sched[j+1], sched[j]
                    move_key = f"reorder_stops_{i}_{j}"
                    neighbors.append((new_solution, move_key))

        return neighbors



    def is_tabu(self, move:str) -> bool:
        """Vérifie si un mouvement est dans la liste taboue"""
        return move in self.tabu_list

    def update_tabu_list(self, move :str):
        """Met à jour la liste taboue"""
        self.tabu_list.append(move)
        if len(self.tabu_list) > self.tabu_size:
            self.tabu_list.pop(0)

    def eval_solution(self, solution: Schedule) -> float:
        """Calcule la fitness d'une solution"""
        total_attente = solution.calculate_waiting_time()
        penalite = 0

        #Pénalité si violations de contraintes
        if not solution.is_valid():
            penalite += 100

        return total_attente + penalite

    def optimize(self) -> Schedule:
        """Execute la recherche taboue pour optimiser l'horaire"""
        logger.info("Starting Tabu Search optimization..")

        current_sol = (copy.deepcopy(self.initial_solution))
        current_fitness = self.eval_solution(current_sol)
        self.best_solution = copy.deepcopy(current_sol)
        self.best_fitness = current_fitness

        for iter in range(self.max_iterations):
            if iter%10 == 0 :
                logger.info(f"Iteration {iter+1}/{self.max_iterations}")
                logger.info(f"Current best fitness: {self.best_fitness}")


            neighborhood = self.get_neighborhood(current_sol)
            best_neighbor = None
            best_neighbor_fitness = float('inf')
            best_move =None


            for neighbor, move in neighborhood:
                if self.is_tabu(move):
                    continue                                        #Ignorer les mouvements tabous

                fitness = self.eval_solution(neighbor)

                #Cirtere d'aspiration: accepter nouveau tabu si meilleur que la la meilleur a present

                if fitness < self.best_fitness:
                    best_neighbor = neighbor
                    best_neighbor_fitness = fitness
                    best_move = move
                    break

                if fitness < best_neighbor_fitness:
                    best_neighbor = neighbor
                    best_neighbor_fitness = fitness
                    best_move = move

            if best_neighbor is None:
                self.non_improving_count += 1
                if self.non_improving_count >= self.max_non_improving:
                    logger.info("Local optima reached. No better neighbors found. ")
                    logger.info("Exiting...")
                    break
                continue

            #rest if improving move found
            if best_neighbor_fitness < current_fitness:
                self.non_improving_count = 0
            else :
                self.non_improving_count += 1

            current_sol = best_neighbor
            current_fitness = best_neighbor_fitness
            self.update_tabu_list(best_move, )

            if best_neighbor_fitness < self.best_fitness:
                self.best_solution = copy.deepcopy(best_neighbor)
                self.best_fitness = best_neighbor_fitness
                logger.info(f"New best solution found with fitness {self.best_fitness}")

        logger.info(f"Tabu Search Completed. Best fitness: {self.best_fitness}")
        return self.best_solution
