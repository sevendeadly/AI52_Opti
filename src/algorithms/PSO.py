"""
Gilles NGASSAM & Daniel KOANGA
09/01/2025
"""

"""
Implements Particle Swarm Optimization for bus schedules.
Updates positions and velocities according to the best local/global solutions.
Key parameters: swarm size, inertia coefficient, cognitive/social factors.

Let's assume between midnight and 6am, there is no bus
"""

# libraries importation
from src.models.plan import Prog, generate_derivated_plan, generate_random_plan, generate_plan_on_peak
from src.models.stations import process_global_waiting_time
from src.models.demand import Demand
from src.utils.constants import NUM_PROGS, PEAK_REPARTITION, MAX_LOCOMOTION_SLOT_VARIATION
from src.utils.time import convertTimeStamp
import random as rd

class ParticleSwarmOptimization:
    def __init__(
            self, 
            num_particles: int, 
            num_iterations: int, 
            inertia_coefficient: float, 
            cognitive_factor: float, 
            social_factor: float, 
            passenger_demands: list[Demand], 
            time_matrix: list[int]
    ):
        """
        PSO class constructor

        Args:
            num_particles (int): number of particles in the swarm
            num_iterations (int): maximum number of iterations
            inertia_coefficient (float): inertia coefficient
            cognitive_factor (float): cognitive factor
            social_factor (float): social factor
            passenger_demands (list[Demand]): list of passengers demand
            time_matrix (list[int]): list of time intervals between each stop
        """
        self.num_particles = num_particles
        self.num_iterations = num_iterations
        self.inertia_coefficient = inertia_coefficient
        self.cognitive_factor = cognitive_factor
        self.social_factor = social_factor
        self.passenger_demands = passenger_demands
        self.time_matrix = time_matrix

    def _initialize_velocities(self) -> list[list[int]]:
        """
        Initialize the velocities of the particles

        Returns:
            list[list[int]]: list of velocities for each particle
        """
        velocities: list[list[int]] = []

        # Initialize velocity with random values
        for _ in range(self.num_particles):
            velocity = [rd.randint(-MAX_LOCOMOTION_SLOT_VARIATION, MAX_LOCOMOTION_SLOT_VARIATION) for _ in range(NUM_PROGS)]
            velocities.append(velocity)
        
        return velocities

    def _update_velocity(
            self, 
            velocity: list[int], 
            particle: list[Prog], 
            personal_best: list[Prog], 
            global_best: list[Prog]
    ) -> list[int]:
        """
        Update the velocity of a particle

        Args:
            velocity (list[int]): current velocity of the particle
            particle (list[Prog]): current position of the particle
            personal_best (list[Prog]): best position of the particle
            global_best (list[Prog]): best position of the swarm

        Returns:
            list[int]: updated velocity of the particle
        """
        # Update velocity based on inertia, cognitive, and social components
        inertia = [self.inertia_coefficient * v for v in velocity]
        cognitive = [self.cognitive_factor * rd.random() * ((p_best.process_tour_start() - p.process_tour_start()) / 60) for p, p_best in zip(particle, personal_best)]
        social = [self.social_factor * rd.random() * ((g_best.process_tour_start() - p.process_tour_start()) / 60) for p, g_best in zip(particle, global_best)]

        float_velocity = [round(i + c + s, 0) for i, c, s in zip(inertia, cognitive, social)]
        velocity = [int(v) for v in float_velocity]

        return velocity

    def _update_position(self, particle: list[Prog], velocity: list[int]) -> list[Prog]:
        """
        Update the position of a particle

        Args:
            particle (list[Prog]): current position of the particle
            velocity (list[int]): velocity of the particle

        Returns:
            list[Prog]: updated position of the particle
        """
        new_position: list[Prog] = particle[:]

        # Update position based on velocity
        for i in range(len(particle)):
            new_position = generate_derivated_plan(new_position, (i, velocity[i], False))
        new_position.sort(key=lambda prog: prog.time)

        return new_position

    def _evaluate(self, particle: list[Prog]) -> int:
        """
        Evaluate the fitness of a particle
        
        Args:
            particle (list[Prog]): the particle to evaluate

        Returns:
            int: the fitness of the particle
        """
        # Evaluate the particle's fitness
        return process_global_waiting_time(particle, self.passenger_demands, self.time_matrix)
    
    def optimize(self) -> list[Prog]:
        # Initialize particles
        tour_duration = sum(self.time_matrix)
        particles: list[list[Prog]] = [generate_plan_on_peak(NUM_PROGS, tour_duration, PEAK_REPARTITION) for _ in range(self.num_particles)]
        velocities: list[list[int]] = self._initialize_velocities()

        personal_best_positions: list[list[Prog]] = particles[:]
        personal_best_scores: list[int] = [self._evaluate(p) for p in particles]
        global_best_position: list[Prog] = personal_best_positions[personal_best_scores.index(min(personal_best_scores))]
        global_best_score: int = min(personal_best_scores)

        for _ in range(self.num_iterations):
            print("Iteration : ", _ + 1, " / ", self.num_iterations)
            for i in range(self.num_particles):
                # Update velocity
                velocities[i] = self._update_velocity(velocities[i], particles[i], personal_best_positions[i], global_best_position)
                # Update position
                particles[i] = self._update_position(particles[i], velocities[i])
                # Evaluate new position
                score = self._evaluate(particles[i])
                # Update personal best
                if score < personal_best_scores[i]:
                    personal_best_positions[i] = particles[i]
                    personal_best_scores[i] = score
                # Update global best
                if score < global_best_score:
                    global_best_position = particles[i]
                    global_best_score = score

            print("Global best score : ", global_best_score)

        return global_best_position