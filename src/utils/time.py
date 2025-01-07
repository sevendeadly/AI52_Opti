"""
Gilles NGASSAM & Daniel KOANGA
31/12/2024
"""
# Librairies importation
from datetime import time
from enum import Enum

# Define the daytime intervals
class DAYTIME(Enum):
    MORNING = 0
    DAY = 1
    EVENING = 2
    NIGHT = 3

# Convert a timestamp in seconds to a time object
def convertTimeStamp(timeStamp: int) -> time:
    """
    Convert a timestamp in seconds to a time object.
    
    Args:
        timeStamp (int): timestamp in seconds

    Returns:
        time: time object
    """
    # Constraint the timestamp to consider time after midnight as the next day
    actual_timeStamp = timeStamp % (24 * 3600)

    hours, minutes, seconds = actual_timeStamp // 3600, (actual_timeStamp % 3600) // 60, actual_timeStamp % 60
    return time(hours, minutes, seconds)