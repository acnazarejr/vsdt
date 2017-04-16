"""SensorDataViewWidget class file."""

#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QCheckBox
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
        self._plots_data = {}
        self._plots_data_groupboxes = {}
        self._start_time = None
        self._end_time = None

        self.gui.splitter.insertWidget(0, self._plot_canvas)
        self._optionslayout = self.gui.optionsLayout
        # self._optionslayout = QVBoxLayout()
        # self.gui.optionsGroup.setLayout(self._optionslayout)

        self.clear()


    def add_plot_data(self, plot_data):
        """add plot data method"""
        self._plots_data[plot_data.data_id] = plot_data
        groupbox, groupbox_checks = self._make_plot_data_groupbox(plot_data)
        self._plots_data_groupboxes[plot_data.data_id] = (groupbox, groupbox_checks)
        self._optionslayout.insertWidget(0, groupbox)
        self._refresh_canvas()

    def _make_plot_data_groupbox(self, plot_data):
        """make plot data groupbox"""
        groupbox = QGroupBox()
        groupbox.setFlat(True)
        groupbox.setCheckable(True)
        groupbox.setChecked(True)
        groupbox.setTitle(plot_data.data_id)
        groupbox.setObjectName(plot_data.data_id)
        layout = QHBoxLayout()
        groupbox_checks = {}
        for key in plot_data.plot_values:
            check = QCheckBox(key)
            check.setObjectName(plot_data.data_id + ':' + key)
            check.setChecked(True)
            check.toggled.connect(self._state_changed)
            groupbox_checks[key] = check
            layout.addWidget(check)
        groupbox.setLayout(layout)
        groupbox.toggled.connect(self._state_changed)
        return groupbox, groupbox_checks

    def clear(self):
        """clear"""
        self._plot_canvas.clear()
        self._plots_data.clear()
        for i in reversed(range(self._optionslayout.count())):
            self._optionslayout.itemAt(i).widget().deleteLater()
        self._plots_data_groupboxes.clear()
        self._start_time = None
        self._end_time = None
    #
    def update_central(self, central):
        """update central"""
        if self._plot_canvas is not None:
            self._plot_canvas.update_central(central)

    def _refresh_canvas(self):
        """refresh canvas"""
        self._plot_canvas.clear()
        valid_plots_data = 0
        for key, plot_data in self._plots_data.items():
            if self._plots_data_groupboxes[key][0].isChecked():
                valid_plots_data += 1
                for valuekey in plot_data.plot_values:
                    value_valid = self._plots_data_groupboxes[key][1][valuekey].isChecked()
                    print(key, valuekey, self._plots_data_groupboxes[key][1][valuekey].isChecked())
                    plot_data.set_plot_value_valid(valuekey, value_valid)

        position = valid_plots_data * 100
        position += 11
        for key, plot_data in self._plots_data.items():
            self._plot_canvas.add_subplot(position, key, plot_data)
            position += 1

    def _state_changed(self, _):
        self._refresh_canvas()

    # def _limits_calculation(self):
    #     """limits calculation"""
    #     starts = []
    #     ends = []
    #     for sensor_data in self._sensors_data.values():
    #         starts.append(sensor_data.start_time)
    #         ends.append(sensor_data.end_time)
    #     self._start_time = min(starts) if starts else None
    #     self._end_time = max(ends) if ends else None
