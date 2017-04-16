"""TemporalData class."""

import datetime
from abc import ABC, abstractmethod
#pylint: disable=E0611
#pylint: disable=E0401
from models.data import Data
from utils.time import time_delta_in_milliseconds
#pylint: enable=E0401
#pylint: enable=E0611

class TemporalData(Data, ABC):
    """Abstract class for temporal data."""

    @abstractmethod
    def __init__(self):
        """Init method"""
        Data.__init__(self)
        self._start_time = None
        self._end_time = None
        self._interval = None

    @property
    def start_time(self):
        """datetime: start_time property."""
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError('start_time must be datetime.datetime')
        if (self._end_time is not None) and (value > self._end_time):
            raise AttributeError('start_time must be lower or equal than end_time')
        self._start_time = value

    @property
    def end_time(self):
        """datetime: end_time property."""
        return self._end_time

    @end_time.setter
    def end_time(self, value):
        if not isinstance(value, datetime.datetime):
            raise TypeError('end_time must be datetime.datetime')
        if (self._start_time is not None) and (value < self._start_time):
            raise AttributeError('end_time must be greater or equal than start_time')
        self._end_time = value

    @property
    def interval(self):
        """float: data interval in milliseconds."""
        return self._interval

    @interval.setter
    def interval(self, value):
        if not isinstance(value, float):
            raise TypeError('interval must be float')
        self._interval = value

    @property
    def length(self):
        """float: data length in milliseconds."""
        if (self._start_time is None) or (self._end_time is None):
            return None
        return time_delta_in_milliseconds(self._end_time, self._start_time)
