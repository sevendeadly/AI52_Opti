import time
import sys

# Fonction pour afficher une barre de progression
def progress_bar(current, total, start_time):
    progress = current / total
    bar_length = 50  # Longueur de la barre
    filled_length = int(bar_length * progress)

    bar = "█" * filled_length + " " * (bar_length - filled_length)
    elapsed_time = time.time() - start_time
    remaining_time = (elapsed_time / progress) - elapsed_time if progress > 0 else 0

    sys.stdout.write(f"\r|{bar}| {progress*100:.2f}% Complete | Elapsed: {elapsed_time:.2f}s | Remaining: {remaining_time:.2f}s")
    sys.stdout.flush()

# Fonction longue simulant une tâche
def long_task(n):
    start_time = time.time()
    for i in range(1, n + 1):
        time.sleep(1)  # Simule un traitement de 1 seconde
        progress_bar(i, n, start_time)

    print("\n✅ Plannification terminée!")

# Programme principal
if __name__ == "__main__":
    total_steps = 10
    long_task(total_steps)
