"""Data class file."""

from abc import ABC, abstractmethod

#pylint: disable=R0903
class Data(ABC):
    """Abstract class for data."""

    @abstractmethod
    def __init__(self):
        """Init method"""
        self._data_id = None

    @property
    def data_id(self):
        """str: Data ID property."""
        return self._data_id

    @data_id.setter
    def data_id(self, value):
        self._data_id = value
