"""SensorDataViewWidget class file."""

#pylint: disable=E0611
#pylint: disable=E0401
from gui.ui import SensorDataViewWidgetUi
from gui.base_widget import BaseWidget
from gui.plot.plot_sensor_canvas import PlotSensorCanvas
#pylint: enable=E0401
#pylint: enable=E0611

class SensorDataViewWidget(BaseWidget):
    """SensorDataViewWidget class."""

    def __init__(self, parent=None):
        """Init method."""
        BaseWidget.__init__(self, parent, SensorDataViewWidgetUi)

        self._plot_canvas = PlotSensorCanvas()
        self._sensors_data = {}

        self.gui.splitter.insertWidget(0, self._plot_canvas)

    def set_sensor_data(self, sensor_data):
        """set sensor data"""
        self._sensors_data[sensor_data.sensor_type] = sensor_data
        self._plot_canvas.add_subplot(111, sensor_data.sensor_type, sensor_data)
        self._plot_canvas.update_central(sensor_data.start_time)

    # def clear(self):
    #     """clear"""
    #     self._plot_canvas.close()
    #     self._plot_canvas = None
    #     self._sensor_data = None

    def update_central(self, central):
        """update central"""
        if self._plot_canvas is not None:
            self._plot_canvas.update_central(central)
