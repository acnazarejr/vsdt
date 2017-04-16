#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""

from gui.ui import SensorDataViewWidgetUi
from gui.base_widget import BaseWidget
from gui.plot import PlotSensorCanvas

class SensorDataViewWidget(BaseWidget):
    """Main Window class"""

    def __init__(self, parent=None):
        """Init method"""
        BaseWidget.__init__(self, parent, SensorDataViewWidgetUi)

        self._plot_canvas = PlotSensorCanvas()
        self._sensor_data = None

        self.gui.splitter.insertWidget(0, self._plot_canvas)

    def set_sensor_data(self, sensor_name, sensor_data):
        """set sensor data"""
        self._sensor_data = sensor_data
        self._plot_canvas.add_subplot(111, sensor_name, sensor_data)
        self._plot_canvas.update_central(sensor_data[0][0])

    # def clear(self):
    #     """clear"""
    #     self._plot_canvas.close()
    #     self._plot_canvas = None
    #     self._sensor_data = None
    #
    def update_central(self, central):
        """update central"""
        if self._plot_canvas is not None:
            self._plot_canvas.update_central(central)
