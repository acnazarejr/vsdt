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

    def __init__(self, zoom=None, central_time=None):
        """Init method"""

        self._figure = Figure()
        self._subplots = {}
        self._subplots_central_lines = {}
        self._plots_data = {}
        self._zoom = zoom
        self._central_time = central_time
        self._start_time = None
        self._end_time = None

        self._figure.subplots_adjust(left=0.08, right=0.99, bottom=0.12, top=0.99,
                                     hspace=0.05, wspace=0)
        self._figure.patch.set_visible(False)
        FigureCanvas.__init__(self, self._figure)
        #pylint: disable=E1101
        FigureCanvas.setSizePolicy(
            self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        #pylint: enable=E1101

    @property
    def zoom(self):
        """zoom property"""
        return self._zoom

    def set_zoom(self, zoom):
        """set xlim shift"""
        self._zoom = zoom
        self._draw_subplots()

    def set_central_time(self, central_time):
        """set central time"""
        self._central_time = central_time
        self._draw_subplots()

    def set_plots_data(self, plots_data):
        """Add subplot."""
        self.clear()
        rows = len(plots_data)
        pos = 1
        for plot_data in plots_data:
            plot_id = plot_data.data_id
            self._subplots[plot_id] = self._figure.add_subplot(rows, 1, pos, facecolor='slategrey')
            self._plots_data[plot_id] = plot_data
            pos += 1
        self._limits_calculation()
        self.refresh_subplots()

    def refresh_subplots(self):
        """Refresh plot"""
        for plot_id in self._subplots:
            self._subplots[plot_id].cla()
            xfmt = md.DateFormatter('%H:%M:%S')
            self._subplots[plot_id].xaxis.set_major_formatter(xfmt)
            timestamps = self._plots_data[plot_id].plot_timestamps
            for valuekey, plot_value in self._plots_data[plot_id].plot_values.items():
                if self._plots_data[plot_id].is_plot_value_valid(valuekey):
                    self._subplots[plot_id].plot(timestamps, plot_value)
        self._draw_subplots()

    def clear(self):
        """Cleal plot canvas."""
        self._figure.clear()
        self._subplots.clear()
        self._plots_data.clear()
        self._subplots_central_lines.clear()
        self._central_time = None
        self._start_time = None
        self._end_time = None

    def _draw_subplots(self):
        """Update figure"""
        if not self._subplots:
            return

        for line in self._subplots_central_lines.values():
            if line:
                line.remove()

        if self._central_time is None:
            average_delta = (self._end_time - self._start_time) / 2
            central_time = self._start_time + average_delta
        else:
            central_time = self._central_time

        for plot_id in self._subplots:
            lim_inf = central_time - datetime.timedelta(milliseconds=self._zoom)
            lim_sup = central_time + datetime.timedelta(milliseconds=self._zoom)
            self._subplots[plot_id].set_xlim(md.date2num(lim_inf), md.date2num(lim_sup))
            central_line = self._subplots[plot_id].axvline(x=md.date2num(central_time), color='red')
            self._subplots_central_lines[plot_id] = central_line
            self.draw()

    def _limits_calculation(self, ):
        starts = []
        ends = []
        for plot_data in self._plots_data.values():
            starts.append(plot_data.plot_timestamps[0])
            ends.append(plot_data.plot_timestamps[-1])
        self._start_time = min(starts) if starts else None
        self._end_time = max(ends) if ends else None
