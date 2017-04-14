#pylint: disable=R0903
"""Data super class"""

from abc import ABC, abstractmethod

class Data(ABC):
    """Abstract class for sensors"""

    @abstractmethod
    def __init__(self):
        """Init method"""
        self._data_id = None

    @property
    def data_id(self):
        """start time property"""
        return self._data_id

    @data_id.setter
    def data_id(self, value):
        """start time property"""
        self._data_id = value
