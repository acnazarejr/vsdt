#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""



from PyQt5 import QtWidgets

from gui.ui import SensorDataFormUi
from gui.base_form import BaseForm
from plot import PlotCanvas


class SensorDataForm(BaseForm):
    """Main Window class"""

    # setupButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Init method"""
        BaseForm.__init__(self, parent, SensorDataFormUi)

        self._plot_canvas = None
        self._sensor_data = None


    def set_sensor_data(self, sensor_data):
        self._sensor_data = sensor_data
        self._plot_canvas = PlotCanvas(self._sensor_data)
        self.gui.viewGroupVerticalLayout.addWidget(self._plot_canvas)

    def update_central(self, central):
        self._plot_canvas.update_central(central)