#pylint: disable=R0903
"""Data super class"""

from abc import ABC, abstractmethod

class Data(ABC):
    """Abstract class for sensors"""

    @abstractmethod
    def __init__(self, data_id=None):
        """Init method"""
        self._id = None

    @property
    def data_id(self):
        """start time property"""
        return self._id
