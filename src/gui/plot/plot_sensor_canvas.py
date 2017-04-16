"""PlotSensorCanvas class file."""

import datetime
from PyQt5 import QtWidgets
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.dates as md

matplotlib.use('Qt5Agg')

class PlotSensorCanvas(FigureCanvas):
    """PlotSensorCanvas class."""

    def __init__(self):
        """Init method"""

        self._figure = Figure()
        self._axes = {}
        self._sensors_data = {}

        self._figure.subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.9, hspace=0, wspace=0)
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)
        #pylint: disable=E1101
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #pylint: enable=E1101

        # self.update_central(sensor_data[100]['timestamp'])

    def add_subplot(self, position, sensor_id, sensor_data):
        """Add subplot."""
        if sensor_data.sensor_type == 'barometer':
            return
        self._axes[sensor_id] = self._figure.add_subplot(position, facecolor='y')
        self._sensors_data[sensor_id] = {}
        if sensor_data.sensor_type in ('accelerometer', 'gyroscope', 'magnetometer'):
            readings = sensor_data.readings
            timestamps, x_values, y_values, z_values = zip(*readings)
            self._sensors_data[sensor_id]['sensor_type'] = sensor_data.sensor_type
            self._sensors_data[sensor_id]['timestamps'] = timestamps
            self._sensors_data[sensor_id]['x'] = x_values
            self._sensors_data[sensor_id]['y'] = y_values
            self._sensors_data[sensor_id]['z'] = z_values

    def update_central(self, central):
        """Update figure"""
        for sensor_id in self._axes:
            self._axes[sensor_id].cla()
            xfmt = md.DateFormatter('%H:%M:%S.%f')
            self._axes[sensor_id].xaxis.set_major_formatter(xfmt)
            lim_inf = central - datetime.timedelta(milliseconds=5000)
            lim_sup = central + datetime.timedelta(milliseconds=5000)
            self._axes[sensor_id].set_xlim(md.date2num(lim_inf), md.date2num(lim_sup))
            self._axes[sensor_id].axvline(x=md.date2num(central), color='red')
            sensor_data = self._sensors_data[sensor_id]
            timestamps = sensor_data['timestamps']
            if sensor_data['sensor_type'] in ('accelerometer', 'gyroscope', 'magnetometer'):
                x_values = sensor_data['x']
                # y_values = sensor_data['y']
                # z_values = sensor_data['z']
                self._axes[sensor_id].plot(timestamps, x_values)
            self.draw()
