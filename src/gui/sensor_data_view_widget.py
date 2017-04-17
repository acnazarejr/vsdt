"""SensorDataViewWidget class file."""

#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtWidgets import QHBoxLayout, QGroupBox, QCheckBox
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

        self._plot_canvas = PlotSensorCanvas(zoom=5000)
        self._plots_data = {}
        self._plots_data_groupboxes = {}

        self.gui.splitter.insertWidget(0, self._plot_canvas)
        self._optionslayout = self.gui.optionsLayout

        self.gui.zoomInButton.clicked.connect(self._zoom_in_button_clicked)
        self.gui.zoomOutButton.clicked.connect(self._zoom_out_button_clicked)

        self.clear()

    def add_plots_data(self, plots_data):
        """add plot data method"""
        for plot_data in plots_data:
            self._plots_data[plot_data.data_id] = plot_data
            groupbox, groupbox_checks = self._make_plot_data_groupbox(plot_data)
            self._plots_data_groupboxes[plot_data.data_id] = (groupbox, groupbox_checks)
            self._optionslayout.insertWidget(0, groupbox)
        self._refresh_plot_canvas()

    def clear(self):
        """clear"""
        self._plot_canvas.clear()
        self._plots_data.clear()
        for i in reversed(range(self._optionslayout.count())):
            self._optionslayout.itemAt(i).widget().deleteLater()
        self._plots_data_groupboxes.clear()
        self._refresh_plot_canvas()

    def update_central_time(self, central_time):
        """update central"""
        self._plot_canvas.set_central_time(central_time)

    def _zoom_in_button_clicked(self):
        self._plot_canvas.set_zoom(self._plot_canvas.zoom - 1000)

    def _zoom_out_button_clicked(self):
        self._plot_canvas.set_zoom(self._plot_canvas.zoom + 1000)

    def _group_state_changed(self, value):
        if value:
            for (groupbox, groupbox_checks) in self._plots_data_groupboxes.values():
                if groupbox.isChecked():
                    all_checked = True
                    for check in groupbox_checks.values():
                        if check.isChecked():
                            all_checked = False
                    if all_checked:
                        for check in groupbox_checks.values():
                            check.setChecked(True)
        self._refresh_plot_canvas()

    def _check_state_changed(self, value):
        if not value:
            for (groupbox, groupbox_checks) in self._plots_data_groupboxes.values():
                if groupbox.isChecked():
                    group_condition = False
                    for check in groupbox_checks.values():
                        if check.isChecked():
                            group_condition = True
                    groupbox.setChecked(group_condition)
        self._refresh_plot_canvas()


    def _make_plot_data_groupbox(self, plot_data):
        """make plot data groupbox"""
        groupbox = QGroupBox()
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
            check.toggled.connect(self._check_state_changed)
            groupbox_checks[key] = check
            layout.addWidget(check)
        groupbox.setLayout(layout)
        groupbox.toggled.connect(self._group_state_changed)
        return groupbox, groupbox_checks

    def _refresh_plot_canvas(self):
        """refresh canvas"""
        self._plot_canvas.clear()
        valid_plots_data = []
        for key, plot_data in self._plots_data.items():
            if self._plots_data_groupboxes[key][0].isChecked():
                for valuekey in plot_data.plot_values:
                    value_valid = self._plots_data_groupboxes[key][1][valuekey].isChecked()
                    plot_data.set_plot_value_valid(valuekey, value_valid)
                valid_plots_data.append(plot_data)
        self._plot_canvas.set_plots_data(valid_plots_data)
