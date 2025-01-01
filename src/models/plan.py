"""
Gilles NGASSAM & Daniel KOANGA
31/12/2024
"""

# Librairies importation
from datetime import time
from src.utils.time import convertTimeStamp

class Prog:
    def __init__(self, time: time, duration: int, direction: bool):
        self.time = time
        self.direction = direction
        self.duration = duration

    # Calculate the start of the prog in seconds
    def process_tour_start(self) -> int:
        return int(self.time.hour * 3600 + self.time.minute * 60 + self.time.second)
    
    # Calculate the end of a the prog in seconds
    def process_tour_end(self) -> int:
        return int(self.process_tour_start() + self.duration)
    
    # Set up a representation of an solution instance
    def __repr__(self):
        return f"Bus - Time: {self.time} - Direction : {"GARE TGV" if self.direction else "VALDOIE "}"
    


class Locomotion:
    def __init__(self, progs: list[Prog]):
        self.progs = progs
    
    # Set up a representation of a locomotion instance
    def __repr__(self):
        return f"Locomotion - reservations: {self.progs}"
    
    # Check if a locomotion is available at a given time
    def is_available(self, new_prog: Prog) -> bool:
        """
        Check if a locomotion is available at a given time according to reservations.

        Args:
            start_time (time): start time of the locomotion
            tour_duration (int): duration of the tour

        Returns:
            bool: True if the locomotion is available, False otherwise
        """
        # Create a fake locomotion with the new prog
        fake_progs = self.progs.copy()
        fake_progs.append(new_prog)
        fake_progs.sort(key=lambda prog: prog.time)
        assumed_index = fake_progs.index(new_prog)
        reservation_start_seconds = new_prog.process_tour_start()
        reservation_end_seconds = new_prog.process_tour_end()

        # Adjust the reservation interval according to directions and durations
        if assumed_index == 0:
            if new_prog.direction == fake_progs[1].direction:
                reservation_end_seconds += new_prog.duration
        elif assumed_index == fake_progs.__len__() - 1:
            if new_prog.direction == fake_progs[-2].direction:
                reservation_start_seconds -= fake_progs[-2].duration
        else:
            if new_prog.direction == fake_progs[assumed_index - 1].direction:
                reservation_start_seconds -= fake_progs[assumed_index - 1].duration
            if new_prog.direction == fake_progs[assumed_index + 1].direction:
                reservation_end_seconds += new_prog.duration
        
        # Check if the reservation interval is available
        for prog in self.progs:
            reservation_start = convertTimeStamp(int(reservation_start_seconds))
            reservation_end = convertTimeStamp(int(reservation_end_seconds))

            prog_end = convertTimeStamp(prog.process_tour_end())
            if prog_end > reservation_start and prog.time < reservation_end:
                    return False

        return True
    
    # Add a new prog to the locomotion
    def add_prog(self, prog: Prog) -> list[Prog]:
        """
        Add a new prog to the locomotion.

        Args:
            prog (Prog): a prog to add to the locomotion

        Returns:
            list[Prog]: the list of progs in the locomotion
        """
        if self.is_available(prog):
            self.progs.append(prog)

        self.sort_progs()

    # Sort the progs in the locomotion by time
    def sort_progs(self) -> list[Prog]:
        """
        Sort the progs in the locomotion by time.

        Returns:
            list[Prog]: the ordonnated list of progs in the locomotion
        """
        self.progs.sort(key=lambda prog: prog.time)

        return self.progs

# Process the required locomotions according to provided plan
def process_required_locomotions(plan: list[Prog]) -> list[Locomotion]:
    """
    Process the required locomotions according to provided plan.

    Args:
        solution (list[Prog]): a list of progs

    Returns:
        list[Locomotion]: the list of required locomotions
    """
    required_locomotions: list[Locomotion] = []

    for prog in plan:
        is_locomotion_found = False

        for locomotion in required_locomotions:
            if locomotion.is_available(prog):
                locomotion.add_prog(prog)
                is_locomotion_found = True
                break
        
        if not is_locomotion_found:
            required_locomotions.append(Locomotion([prog]))

    return required_locomotions

# Check if a plan is valid according to locomotion fleet
def is_valid_plan(plan: list[Prog], max_num_locomotions: int) -> bool:
    """
    Check if a plan is valid.

    Args:
        plan (list[Prog]): a list of progs

    Returns:
        bool: True if the plan is valid, False otherwise
    """
    locomotions = process_required_locomotions(plan)

    return locomotions.__len__() <= max_num_locomotions