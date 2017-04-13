#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Base form class file"""

from abc import abstractmethod
from PyQt5 import QtCore
from gui.base_widget import BaseWidget

class BaseMDIWidget(BaseWidget):
    """Base Form class"""

    title_updated = QtCore.pyqtSignal(object)

    @abstractmethod
    def __init__(self, parent, decorator):
        """init method"""
        BaseWidget.__init__(self, parent, decorator)
        self._has_changes = False

    @abstractmethod
    def get_title(self):
        """Abstract get_name method"""
        pass

    @abstractmethod
    def get_icon(self):
        """Abstract get_icon method"""
        pass

    @property
    def has_changes(self):
        """start time property"""
        return self._has_changes
