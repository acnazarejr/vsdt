"""Base Canvas class"""

import numpy as np
import random
import datetime
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as md

 # Make sure that we are using QT5
matplotlib.use('Qt5Agg')

class PlotCanvas(FigureCanvas):
    """Base canvas class"""

    def __init__(self, sensor_data):
        """Init method"""

        self._sensor_data = sensor_data

        self._timestamps = [item['timestamp'] for item in sensor_data]
        self._timestamps = md.date2num(self._timestamps)
        self._x_values = [item['values']['x'] for item in sensor_data]

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

        # self.update_central(sensor_data[100]['timestamp'])

    def update_central(self, central):
        """Update figure"""
        self._axes.cla()
        xfmt = md.DateFormatter('%H:%M:%S.%f')
        self._axes.xaxis.set_major_formatter(xfmt)
        lim_inf = central - datetime.timedelta(milliseconds=5000)
        lim_sup = central + datetime.timedelta(milliseconds=5000)
        self._axes.set_xlim(md.date2num(lim_inf), md.date2num(lim_sup))
        self._axes.axvline(x=md.date2num(central), color='red')
        self._axes.plot(self._timestamps, self._x_values)
        self.draw()
