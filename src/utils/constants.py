# This file contains all the constants used in the program

# librairies import
from src.utils.time import DAYTIME

# all the constraints definitions to run the program (time in minutes)
NUM_STOPS = 18
LOCOMOTION_CAPACITY = 80
SERVICE_START = 6 * 60
SERVICE_END = 24 * 60
MIN_TIME_BETWEEN_STOPS = 1
MAX_TIME_BETWEEN_STOPS = 5
NUM_LOCOMOTIONS = 200
PASSENGERS_DEMAND = 1000
NUM_PROGS = 100
DIRECTION_REPARTITION = (50, 50)
PEAK_REPARTITION = [(DAYTIME.MORNING, 35), (DAYTIME.DAY, 20), (DAYTIME.EVENING, 35), (DAYTIME.NIGHT, 10)]
PEAK_TIME_INTERVALS = [(SERVICE_START, 10 * 60), (10 * 60, 16 * 60), (16 * 60, 20 * 60), (20 * 60, SERVICE_END)]
MAX_PROG_VARIATION = 5
DEMAND_INSTANCE_HEADERS = ['Arrival time', 'Boarding stop', 'Stops to go', 'Direction']
PLAN_INSTANCE_HEADERS = ['Direction', 'Departure Time', 'Duration (minutes)']
UP_TERMINUS = "Gare TGV"
DOWN_TERMINUS = "VALDOIE "