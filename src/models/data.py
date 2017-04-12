"""Data super class"""

from abc import ABC, abstractmethod

class Data(ABC):
    """Abstract class for sensors"""

    @abstractmethod
    def __init__(self):
        """Init method"""
        self._interval = None
        self._length = None
        self._start_time = None
        self._end_time = None

    @property
    def start_time(self):
        """start time property"""
        return self._start_time

    @property
    def end_time(self):
        """end time property"""
        return self._end_time

    @property
    def interval(self):
        """start time property"""
        return self._interval

    @property
    def length(self):
        """length property"""
        return self._length
