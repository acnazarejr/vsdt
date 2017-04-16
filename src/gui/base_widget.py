"""Base widget class file."""

from abc import abstractmethod
#pylint: disable=E0611
from PyQt5.QtWidgets import QWidget
#pylint: enable=E0611

#pylint: disable=R0903
class BaseWidget(QWidget):
    """BaseWidget class."""

    @abstractmethod
    def __init__(self, parent, decorator):
        """init method"""
        QWidget.__init__(self, parent)
        self.gui = decorator()
        self.gui.setupUi(self)
        #pylint: enable=E1101
