"""Base MDI class file."""

#pylint: disable=E0611
#pylint: disable=E0401
from abc import abstractmethod
from PyQt5 import QtCore
from gui.base_widget import BaseWidget
#pylint: enable=E0401
#pylint: enable=E0611

class BaseMDI(BaseWidget):
    """BaseMDI class."""

    #pylint: disable=E1101
    title_updated = QtCore.pyqtSignal(object)
    #pylint: enable=E1101

    @abstractmethod
    def __init__(self, parent, decorator):
        """Init method."""
        BaseWidget.__init__(self, parent, decorator)
        self._has_changes = False
        self._working_dir = None

    @abstractmethod
    def get_title(self):
        """Abstract get_title method"""
        raise NotImplementedError('abstract method')

    @staticmethod
    @abstractmethod
    def get_icon():
        """Abstract get_icon method"""
        raise NotImplementedError('abstract method')

    @property
    def has_changes(self):
        """bool: returns if mdi has changes or not"""
        return self._has_changes

    @has_changes.setter
    def has_changes(self, value):
        self._has_changes = value

    @property
    def working_dir(self):
        """string: returns the mdi working dir"""
        return self._working_dir

    @working_dir.setter
    def working_dir(self, value):
        self._working_dir = value
