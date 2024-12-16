# src/models/schedule.py
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)


class BusStop:
    def __init__(self, id: int, name: str, demand: Dict[str, int]):
        """
        Initialize a bus stop with its properties.

        Args:
            id: Unique identifier for the stop
            name: Name of the stop
            demand: Dictionary mapping time periods to passenger demand
        """
        self.id = id
        self.name = name
        self.demand = demand  # Example: {'morning': 50, 'afternoon': 30, 'evening': 20}


class Bus:
    def __init__(self, id: int, capacity: int):
        """
        Initialize a bus with its properties.

        Args:
            id: Unique identifier for the bus
            capacity: Maximum passenger capacity
        """
        self.id = id
        self.capacity = capacity
        self.schedule = []  # List of dictionaries with stop_id and time


class Schedule:
    def __init__(self, buses: List[Bus], stops: List[BusStop]):
        """
        Initialize a schedule with buses and stops.

        Args:
            buses: List of Bus objects
            stops: List of BusStop objects
        """
        self.buses = buses
        self.stops = stops
        self.time_periods = {
            'morning': (360, 720),  # 6:00 - 12:00
            'afternoon': (720, 1080),  # 12:00 - 18:00
            'evening': (1080, 1440)  # 18:00 - 24:00
        }

    def calculate_waiting_time(self) -> float:
        """Calculate total weighted waiting time across all stops."""
        total_waiting_time = 0.0

        for stop in self.stops:
            # Collect all service times for this stop
            service_times = []
            for bus in self.buses:
                for service in bus.schedule:
                    if service['stop_id'] == stop.id:
                        service_times.append(service['time'])

            if not service_times:
                # Penalize unserved stops heavily
                total_waiting_time += 1000
                continue

            service_times.sort()

            # Calculate waiting times between consecutive services
            for i in range(len(service_times) - 1):
                time_gap = service_times[i + 1] - service_times[i]
                period = self.get_time_period(service_times[i])
                if period in stop.demand:
                    total_waiting_time += time_gap * stop.demand[period]

        return total_waiting_time

    def is_valid(self) -> bool:
        """Check if the schedule satisfies all constraints."""
        try:
            # Check capacity constraints
            if not self._check_capacity_constraints():
                return False

            # Check timing constraints
            if not self._check_timing_constraints():
                return False

            # Check service coverage
            if not self._check_service_coverage():
                return False

            return True

        except Exception as e:
            logger.error(f"Error validating schedule: {str(e)}")
            return False

    def _check_capacity_constraints(self) -> bool:
        """Verify that bus capacity constraints are not violated."""
        for bus in self.buses:
            for service in bus.schedule:
                stop_id = service['stop_id']
                time = service['time']
                period = self.get_time_period(time)

                stop = next((s for s in self.stops if s.id == stop_id), None)
                if stop and period in stop.demand:
                    if stop.demand[period] > bus.capacity:
                        return False
        return True

    def _check_timing_constraints(self) -> bool:
        """Verify that timing constraints between stops are respected."""
        MIN_TRAVEL_TIME = 10  # Minimum minutes between stops

        for bus in self.buses:
            schedule = sorted(bus.schedule, key=lambda x: x['time'])
            for i in range(len(schedule) - 1):
                time_diff = schedule[i + 1]['time'] - schedule[i]['time']
                if time_diff < MIN_TRAVEL_TIME:
                    return False
        return True

    def _check_service_coverage(self) -> bool:
        """Verify that all stops receive some service."""
        served_stops = set()
        for bus in self.buses:
            for service in bus.schedule:
                served_stops.add(service['stop_id'])

        return len(served_stops) == len(self.stops)

    def get_time_period(self, time: int) -> str:
        """Convert time (in minutes from midnight) to period of day."""
        for period, (start, end) in self.time_periods.items():
            if start <= time < end:
                return period
        return 'evening'  # Default period for times outside defined ranges

    @classmethod
    def deserialize(cls, filepath: str) -> 'Schedule':
        """Create a Schedule instance from a JSON file."""
        try:
            with open(filepath, 'r') as file:
                data = json.load(file)

            stops = [BusStop(
                id=stop['id'],
                name=stop['name'],
                demand=stop['demand']
            ) for stop in data['stops']]

            buses = [Bus(
                id=bus['id'],
                capacity=bus['capacity']
            ) for bus in data['buses']]

            # Load schedules
            for bus_data, bus in zip(data['buses'], buses):
                bus.schedule = bus_data.get('schedule', [])

            return cls(buses=buses, stops=stops)

        except Exception as e:
            logger.error(f"Error deserializing schedule from {filepath}: {str(e)}")
            raise