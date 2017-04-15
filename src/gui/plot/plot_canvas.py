"""Base Canvas class"""

import numpy as np
import random
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

 # Make sure that we are using QT5
matplotlib.use('Qt5Agg')

class PlotCanvas(FigureCanvas):
    """Base canvas class"""

    def __init__(self, sensor_data):
        """Init method"""


        self._timestamps = np.arange(0, 10000, 0.2)
        self._x_values = [random.randint(0, 10) for i in range(len(self._timestamps))]
        self._y_values = [random.randint(0, 10) for i in range(len(self._timestamps))]
        self._z_values = [random.randint(0, 10) for i in range(len(self._timestamps))]

        # self._sensor_data = sensor_data

        self._figure = Figure()
        self._figure.subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.9, hspace=0, wspace=0)
        self._axes = self._figure.add_subplot(111)

        FigureCanvas.__init__(self, self._figure)

        #pylint: disable=E1101
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #pylint: enable=E1101

        self.update_central(1000)

    def update_central(self, central):
        """Update figure"""
        self._axes.cla()
        self._axes.set_xlim(central-200, central+200)
        self._axes.axvline(x=central, color='red')
        self._axes.plot(self._timestamps, self._x_values)
        self.draw()
