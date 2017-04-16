"""PlotData class file."""

#pylint: disable=E0611
#pylint: disable=E0401
from models.data import Data
#pylint: enable=E0401
#pylint: enable=E0611

class PlotData(Data):
    """Sensor Data class"""

    def __init__(self, data_id, plot_timestamps, plot_values, valid_plot_values=None):
        """Init method."""
        Data.__init__(self)

        for value in plot_values.values():
            if len(plot_timestamps) != len(value):
                raise AssertionError('The size of timestamps and values[] must be same')

        self._data_id = data_id
        self._plot_timestamps = plot_timestamps
        self._plot_values = plot_values
        if valid_plot_values is None:
            valid_plot_values = {}
            for key in plot_values:
                valid_plot_values[key] = True
        self._valid_plot_values = valid_plot_values

    def set_plot_value_valid(self, plot_value_id, valid=True):
        """Set plot valu valid."""
        self._valid_plot_values[plot_value_id] = valid

    def is_plot_value_valid(self, plot_value_id):
        """is plot valu valid."""
        return self._valid_plot_values[plot_value_id]

    @property
    def plot_timestamps(self):
        """Timestamps property."""
        return self._plot_timestamps

    @property
    def plot_values(self):
        """Values property"""
        return self._plot_values
