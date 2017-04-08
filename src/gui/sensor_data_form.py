#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""

import random

from PyQt5 import QtCore, QtGui
from PyQt5 import QtWidgets

from gui.ui import SensorDataFormUi
from gui.base_form import BaseForm
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt


class SensorDataForm(BaseForm):
    """Main Window class"""

    # setupButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Init method"""
        BaseForm.__init__(self, parent, SensorDataFormUi)

        # a figure instance to plot on
        self.figure = plt.figure()

        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.button = QtWidgets.QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        # layout = QtWidgets.QVBoxLayout()
        self.gui.viewGroupVerticalLayout.addWidget(self.toolbar)
        self.gui.viewGroupVerticalLayout.addWidget(self.canvas)
        self.gui.viewGroupVerticalLayout.addWidget(self.button)

        # self.gui.setLayout(layout)

    def plot(self):
        ''' plot some random stuff '''
        # random data
        data = [random.random() for i in range(10)]

        # create an axis
        ax = self.figure.add_subplot(111)

        # # discards the old graph
        # ax.hold(False)

        # plot data
        ax.plot(data, '*-')

        # refresh canvas
        self.canvas.draw()
