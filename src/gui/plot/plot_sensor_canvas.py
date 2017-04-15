"""Base Canvas class"""

# import numpy as np
# import random
import datetime
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as md

 # Make sure that we are using QT5
matplotlib.use('Qt5Agg')

class PlotSensorCanvas(FigureCanvas):
    """Base canvas class"""

    def __init__(self):
        """Init method"""

        # self._sensor_data = sensor_data

        # self._timestamps = [item['timestamp'] for item in sensor_data]
        # self._timestamps = md.date2num(self._timestamps)
        # self._x_values = [item['values']['x'] for item in sensor_data]

        # self._sensor_data = sensor_data

        self._figure = Figure()
        self._axes = {}
        self._data = {}
    #self._figure.subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.9, hspace=0, wspace=0)
        self._figure.patch.set_visible(False)
        # self._axes = self._figure.add_subplot(111, facecolor='y')
        # self._figure.tight_layout()

        FigureCanvas.__init__(self, self._figure)

        #pylint: disable=E1101
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #pylint: enable=E1101

        # self.update_central(sensor_data[100]['timestamp'])
        self.draw()

    def add_subplot(self, position, sensor_name, sensor_data):
        """add subplot"""
        self._axes[sensor_name] = self._figure.add_subplot(position, facecolor='y')
        self._data[sensor_name] = {}
        if sensor_name in ('accelerometer', 'gyroscope', 'magnetometer'):
            timestamps, x_values, y_values, z_values = zip(*sensor_data)
            self._data[sensor_name]['timestamps'] = timestamps
            self._data[sensor_name]['x'] = x_values
            self._data[sensor_name]['y'] = y_values
            self._data[sensor_name]['z'] = z_values

    def update_central(self, central):
        """Update figure"""
        for sensor_name in self._axes:
            self._axes[sensor_name].cla()
            xfmt = md.DateFormatter('%H:%M:%S.%f')
            self._axes[sensor_name].xaxis.set_major_formatter(xfmt)
            lim_inf = central - datetime.timedelta(milliseconds=5000)
            lim_sup = central + datetime.timedelta(milliseconds=5000)
            self._axes[sensor_name].set_xlim(md.date2num(lim_inf), md.date2num(lim_sup))
            self._axes[sensor_name].axvline(x=md.date2num(central), color='red')
            self._axes[sensor_name].plot(self._data[sensor_name]['timestamps'],
                                         self._data[sensor_name]['x'],
                                         self._data[sensor_name]['y'],
                                         self._data[sensor_name]['z'])
            self.draw()
