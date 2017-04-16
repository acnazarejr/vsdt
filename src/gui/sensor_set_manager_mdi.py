"""SensorSetManagerMDI class file."""

import os
import dateutil.parser
#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QTreeWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
from gui.base_mdi import BaseMDI
from gui.ui import SensorSetManagerMDIUi
from gui.sensor_data_view_widget import SensorDataViewWidget
from gui.time_control_widget import TimeControlWidget
from gui.gui_utils import save_message_box, get_save_file, get_open_files
from gui.plot.plot_data import PlotData
from models.sensor_data import SENSORTYPES, SENSORTYPES_VALUES_SIZES
#pylint: enable=E0401
#pylint: enable=E0611

class SensorSetManagerMDI(BaseMDI):
    """Main Window class"""

    ###############################################################################################
    # Init Method
    ###############################################################################################
    def __init__(self, sensor_set_data, working_dir=None, has_changes=False, parent=None):
        """Init method"""
        BaseMDI.__init__(self, parent, SensorSetManagerMDIUi)

        self._sensor_set_data = sensor_set_data
        self._working_dir = working_dir
        self._has_changes = has_changes
        self._sensor_data_view_widget = None
        self._time_control_widget = None
        self._json_file = None

        self._configure_gui()
        self._fill_fields()
        self._make_connections()

    ###############################################################################################
    # Public Methods
    ###############################################################################################
    def get_title(self):
        """Get window name"""
        title = self._sensor_set_data.data_id
        return title if not self._has_changes else title + '*'

    @staticmethod
    def get_icon():
        """get icon"""
        return QIcon(':/icons/sensor_manager.png')

    def set_json_file(self, json_file):
        """Set json file."""
        self._json_file = json_file

    ###############################################################################################
    # Private Methods
    ###############################################################################################
    def _configure_gui(self):
        self.gui.verticalSplitter.setStretchFactor(0, 1)
        self.gui.verticalSplitter.setStretchFactor(1, 8)
        self.gui.optionsSplitter.setStretchFactor(0, 1)
        self.gui.optionsSplitter.setStretchFactor(1, 8)

        self._sensor_data_view_widget = SensorDataViewWidget()
        self._time_control_widget = TimeControlWidget()
        layout = QVBoxLayout()
        layout.addWidget(self._sensor_data_view_widget)
        layout.addWidget(self._time_control_widget)
        self.gui.dataVisualizationGroup.setLayout(layout)

        self._tree_parent_device = QTreeWidgetItem(self.gui.sensorDataTree)
        self._tree_parent_device.setExpanded(True)
        self._tree_parent_device.setFlags(Qt.ItemIsEnabled)
        self._refresh_tree_view()

        self._data_view_refresh()

    def _fill_fields(self):
        self.gui.dataIDField.setText(self._sensor_set_data.data_id)
        self.gui.deviceNameField.setText(self._sensor_set_data.device_name)
        self.gui.deviceLocationField.setText(self._sensor_set_data.device_location)
        device_type = self._sensor_set_data.device_type
        index = self.gui.deviceTypeList.findText(device_type, Qt.MatchFixedString)
        if index >= 0:
            self.gui.deviceTypeList.setCurrentIndex(index)

    def _make_connections(self):
        self.gui.dataIDField.textChanged.connect(self._data_id_field_changed)
        self.gui.deviceNameField.textChanged.connect(self._device_name_field_changed)
        self.gui.deviceLocationField.textChanged.connect(self._device_location_field_changed)
        self.gui.deviceTypeList.currentIndexChanged.connect(self._device_type_list_changed)
        self.gui.saveButton.clicked.connect(self._save_button_clicked)
        self.gui.addSensorButton.clicked.connect(self._add_sensor_button_clicked)
        self.gui.deleteSensorButton.clicked.connect(self._delete_sensor_button_clicked)
        self.gui.sensorDataTree.itemSelectionChanged.connect(self._sensor_tree_selection_changed)
        self._time_control_widget.time_updated.connect(self._time_updated)

    def _update_tree_view(self):
        self._tree_parent_device.setText(0, self._sensor_set_data.device_name)
        if self._sensor_set_data.device_type == 'smartphone':
            self._tree_parent_device.setIcon(0, QIcon(':/icons/smartphone.png'))
        if self._sensor_set_data.device_type == 'smartwatch':
            self._tree_parent_device.setIcon(0, QIcon(':/icons/smartwatch.png'))

    def _refresh_tree_view(self):
        self._update_tree_view()
        self._tree_parent_device.takeChildren()
        for sensor_data in self._sensor_set_data.sensors_data:
            child = QTreeWidgetItem(self._tree_parent_device)
            child_text = '{} ({} values)'.format(sensor_data.sensor_type, len(sensor_data.readings))
            child.setText(0, child_text)
            child.setText(1, sensor_data.sensor_type)
            child.setIcon(0, QIcon(':/icons/sensor.png'))

    def _save(self):
        if len(self._sensor_set_data.sensors_data) == 0:
            confirm_save = QMessageBox.warning(self, "Alert", \
                "This data does not have any sensor. Do you want save?",  \
                QMessageBox.Ok | QMessageBox.Cancel)
            if confirm_save == QMessageBox.Cancel:
                return False

        if self._json_file is not None:
            self._sensor_set_data.save(self._json_file)
            self._has_changes = False
        else:
            suggestion = os.path.join(self._working_dir, self._sensor_set_data.data_id + '.json')
            json_file = get_save_file(self, 'Save file', "JSON Files (*.json)", suggestion)
            if json_file is None:
                return False
            self._sensor_set_data.save(json_file)
            self._json_file = json_file
            self._has_changes = False
        return True

    def _data_view_refresh(self):
        self._sensor_data_view_widget.clear()
        selected_itens = self.gui.sensorDataTree.selectedItems()
        if selected_itens:
            selected_sensors_data = []
            for selected_item in selected_itens:
                sensor_type = selected_item.text(1)
                selected_sensors_data.append(self._sensor_set_data.get_sensor_data(sensor_type))
            self._update_time_control(selected_sensors_data)
            self._time_control_widget.set_enable(True)
            self._time_control_widget.show()
            self._sensor_data_view_widget.show()
            for sensor_data in selected_sensors_data:
                plot_data = self._make_plot_data(sensor_data)
                if plot_data is not None:
                    self._sensor_data_view_widget.add_plot_data(plot_data)
        else:
            self._sensor_data_view_widget.hide()
            self._time_control_widget.set_enable(False)
            self._time_control_widget.hide()

    @staticmethod
    def _make_plot_data(sensor_data):
        """make plot data"""
        readings = sensor_data.readings
        timestamps = None
        values = None
        if sensor_data.sensor_type in ('accelerometer', 'gyroscope', 'magnetometer'):
            timestamps, x_values, y_values, z_values = zip(*readings)
            values = {}
            values['x'] = x_values
            values['y'] = y_values
            values['z'] = z_values
            return PlotData(sensor_data.sensor_type, timestamps, values)
        elif sensor_data.sensor_type == 'barometer':
            timestamps, hpa_values = zip(*readings)
            values = {}
            values['hpa'] = hpa_values
            return PlotData(sensor_data.sensor_type, timestamps, values)
        else:
            return None




    def _update_time_control(self, selected_sensors_data):
        """update time control"""
        starts = []
        ends = []
        intervals = []
        for sensor_data in selected_sensors_data:
            starts.append(sensor_data.start_time)
            ends.append(sensor_data.end_time)
            intervals.append(sensor_data.interval)
        start_time = min(starts) if starts else None
        end_time = max(ends) if ends else None
        interval = min(intervals) if intervals else None
        self._time_control_widget.set_control_values(start_time=start_time,
                                                     end_time=end_time,
                                                     interval=interval)

    ###############################################################################################
    # Private Slots
    ###############################################################################################
    def _data_id_field_changed(self, new_data_id):
        self._has_changes = True
        self._sensor_set_data.data_id = new_data_id
        self.title_updated.emit(self.get_title())
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _device_name_field_changed(self, new_device_name):
        self._has_changes = True
        self._sensor_set_data.device_name = new_device_name
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _device_location_field_changed(self, new_location_name):
        self._has_changes = True
        self._sensor_set_data.device_location = new_location_name
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _device_type_list_changed(self):
        self._has_changes = True
        self._sensor_set_data.device_type = self.gui.deviceTypeList.currentText()
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _save_button_clicked(self):
        self._save()
        self.title_updated.emit(self.get_title())

    def _add_sensor_button_clicked(self):
        sensor_data_files = get_open_files(self, 'Open Sensor Files', 'Text File (*.txt)')
        for sensor_data_file in sensor_data_files:
            sensor_type, readings = self._process_sensor_data_file(sensor_data_file)
            if self._sensor_set_data.has_sensor(sensor_type):
                QMessageBox.critical(self, "Alert", \
                    "This sensor data already has the {} sensor".format(sensor_type), \
                    QMessageBox.Ok)
            else:
                self._has_changes = True
                self._sensor_set_data.add_sensor_data(sensor_type, readings)
                self._refresh_tree_view()
                self.title_updated.emit(self.get_title())

    def _delete_sensor_button_clicked(self):
        confirm_delete = QMessageBox.warning(self, "Alert", \
            "Want to delete?", QMessageBox.Ok | QMessageBox.Cancel)
        if confirm_delete == QMessageBox.Ok:
            selected_itens = self.gui.sensorDataTree.selectedItems()
            for item in selected_itens:
                self._has_changes = True
                self._sensor_set_data.remove_sensor_data(item.text(1))
                self._refresh_tree_view()
                self.title_updated.emit(self.get_title())

    def _sensor_tree_selection_changed(self):
        selected_itens = self.gui.sensorDataTree.selectedItems()
        if not selected_itens:
            self.gui.deleteSensorButton.setEnabled(False)
        else:
            self.gui.deleteSensorButton.setEnabled(True)
        self._data_view_refresh()

    def _time_updated(self, time):
        """control current updated slot"""
        self._sensor_data_view_widget.update_central(time)



    ###############################################################################################
    # Protected auxiliar method
    ###############################################################################################
    def _process_sensor_data_file(self, sensor_data_file):
        """process a text file with sensor data"""

        if not os.path.isfile(sensor_data_file):
            QMessageBox.critical(self, 'Error', 'File not found: {}', QMessageBox.Ok)

        sensor_type = None
        for s_type in SENSORTYPES:
            if s_type in sensor_data_file:
                sensor_type = s_type

        if sensor_type is None:
            QMessageBox.critical(self, 'Error', 'Invalid sensor type: {}', QMessageBox.Ok)
            return None, None

        readings = []
        for line in open(sensor_data_file):
            reading = line.split(';')
            if len(reading) != (SENSORTYPES_VALUES_SIZES[sensor_type] + 1):
                QMessageBox.critical(self, 'Error', 'Invalid sensor type: {}', QMessageBox.Ok)
                return None, None
            reading[0] = dateutil.parser.parse(reading[0])
            for idx in range(1, len(reading)):
                reading[idx] = float(reading[idx].replace(',', '.'))
            readings.append(reading)

        return sensor_type, readings

    ###############################################################################################
    # Override methods
    ###############################################################################################
    #pylint: disable=C0103
    def closeEvent(self, event):
        """close event"""
        if not self._has_changes:
            event.accept()
        else:
            save_question = save_message_box(self)
            if save_question == QMessageBox.Save:
                if self._save():
                    event.accept()
                else:
                    event.ignore()
            elif save_question == QMessageBox.Cancel:
                event.ignore()
            elif save_question == QMessageBox.Discard:
                event.accept()
    #pylint: enable=C0103
