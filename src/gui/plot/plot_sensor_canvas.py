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
        self._subplots = {}
        self._centralLines = {}
        self._plots_data = {}

        self._figure.subplots_adjust(left=0.1, right=0.99, bottom=0.1, top=0.9, hspace=0, wspace=0)
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)
        #pylint: disable=E1101
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #pylint: enable=E1101

        # self.update_central(sensor_data[100]['timestamp'])

    def add_subplot(self, position, plot_id, plot_data):
        """Add subplot."""
        self._subplots[plot_id] = self._figure.add_subplot(position, facecolor='y')
        self._plots_data[plot_id] = plot_data
        self.refresh_plot()


    def refresh_plot(self):
        """Refresh plot"""
        for plot_id in self._subplots:
            self._subplots[plot_id].cla()
            xfmt = md.DateFormatter('%H:%M:%S.%f')
            self._subplots[plot_id].xaxis.set_major_formatter(xfmt)
            timestamps = self._plots_data[plot_id].plot_timestamps
            for valuekey, plot_value in self._plots_data[plot_id].plot_values.items():
                print(valuekey)
                if self._plots_data[plot_id].is_plot_value_valid(valuekey):
                    self._subplots[plot_id].plot(timestamps, plot_value)
            self.draw()

    def clear(self):
        """Cleal plot canvas."""
        self._figure.clear()
        self._subplots.clear()
        self._plots_data.clear()


    def update_central(self, central):
        """Update figure"""
        for line in self._centralLines.values():
            line.remove()
        for plot_id in self._subplots:
            lim_inf = central - datetime.timedelta(milliseconds=5000)
            lim_sup = central + datetime.timedelta(milliseconds=5000)
            self._subplots[plot_id].set_xlim(md.date2num(lim_inf), md.date2num(lim_sup))
            self._centralLines[plot_id] = self._subplots[plot_id].axvline(x=md.date2num(central), color='red')
            self.draw()
