"""
Gilles NGASSAM & Daniel KOANGA
31/12/2024
"""
# Librairies importation
from datetime import time

# Convert a timestamp in seconds to a time object
def convertTimeStamp(timeStamp: int) -> time:
    """
    Convert a timestamp in seconds to a time object.
    
    Args:
        timeStamp (int): timestamp in seconds

    Returns:
        time: time object
    """
    hours, minutes, seconds = timeStamp // 3600, (timeStamp % 3600) // 60, timeStamp % 60
    return time(hours, minutes, seconds)