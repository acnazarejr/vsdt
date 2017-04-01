#pylint: disable=E1101
"""Base form class file"""

from abc import abstractmethod

from PyQt5 import QtWidgets

class BaseForm(QtWidgets.QWidget):
    """Base Form class"""

    @abstractmethod
    def __init__(self, parent, decorator):
        """init method"""
        QtWidgets.QWidget.__init__(self, parent)
        self.gui = decorator()
        self.gui.setupUi(self)

    @abstractmethod
    def update(self):
        """Abstract update method"""
        pass

    @abstractmethod
    def clean(self):
        """Abstract clean method"""
        pass
