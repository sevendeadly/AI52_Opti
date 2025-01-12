"""
Gilles NGASSAM & Daniel KOANGA
09/01/2025
"""

# libraries importation
import time
import sys

class Logger:
    def __init__(self, total_steps: int, bar_length: int=20):
        """
        Initialize the Logger with the given parameters

        Args:
            total_steps (int): Total number of steps
            bar_length (int): Length of the progress bar
        
        """
        self.total_steps = total_steps
        self.current_step = 0
        self.best_solution: float = float('inf')
        self.start_time = time.time()
        self.bar_length = bar_length

    def update(self, best_solution: float) -> None:
        """
        Update the logger with the best solution found and increment the loader bar
        
        Args:
            best_solution (float): The best solution found
        """
        self.current_step += 1
        self.best_solution = best_solution * 60 * 60
        self.display()

        if(self.current_step == self.total_steps):
            self.complete()

    def display(self) -> None:
        """
        Display the progress bar
        """
        progress = self.current_step / self.total_steps
        filled_length = int(self.bar_length * progress)
        bar = "█" * filled_length + " " * (self.bar_length - filled_length)
        elapsed_time = time.time() - self.start_time

        minutes, seconds = int(self.best_solution // 60), int(self.best_solution % 60)

        sys.stdout.write(f"\r|{bar}| {progress*100:.2f}% Done | Time: {elapsed_time:.2f}s | {minutes} mins {seconds} secs")
        sys.stdout.flush()

    def complete(self):
        print("\nOptimization completed ✅!")