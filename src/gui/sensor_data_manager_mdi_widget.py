#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
#pylint: disable=R0903
#pylint: disable=C0412
"""Main Window class"""

import os
import dateutil.parser
from PyQt5 import QtGui, QtWidgets, QtCore
from gui import utils
from gui.ui import SensorDataManagerMDIWidgetUi
from gui.base_mdi_widget import BaseMDIWidget
from models.sensor_data import SensorType
from gui.time_control_widget import TimeControlWidget
from gui.sensor_data_view_widget import SensorDataViewWidget
import control.utils

class SensorDataManagerMDIWidget(BaseMDIWidget):
    """Main Window class"""

    def __init__(self, sensor_data, working_dir=None, has_changes=False, parent=None):
        """Init method"""
        BaseMDIWidget.__init__(self, parent, SensorDataManagerMDIWidgetUi)

        self._sensor_data = sensor_data
        self._working_dir = working_dir
        self._has_changes = has_changes

        self.gui.verticalSplitter.setStretchFactor(0, 1)
        self.gui.verticalSplitter.setStretchFactor(1, 8)
        self.gui.optionsSplitter.setStretchFactor(0, 1)
        self.gui.optionsSplitter.setStretchFactor(1, 8)

        self._sensor_data_view_widget = SensorDataViewWidget()
        self._time_control_widget = TimeControlWidget()
        self._dataVisualizationGroupBoxLayout = QtWidgets.QVBoxLayout()
        self._dataVisualizationGroupBoxLayout.addWidget(self._sensor_data_view_widget)
        self._dataVisualizationGroupBoxLayout.addWidget(self._time_control_widget)
        self.gui.dataVisualizationGroupBox.setLayout(self._dataVisualizationGroupBoxLayout)
        self._time_control_widget.time_updated.connect(self._time_updated)
        self._data_view_refresh()

        self.gui.dataIDField.setText(self._sensor_data.data_id)
        self.gui.dataIDField.textChanged.connect(self._data_id_field_changed)

        self.gui.deviceNameField.setText(self._sensor_data.device_name)
        self.gui.deviceNameField.textChanged.connect(self._device_name_field_changed)

        device_type = self._sensor_data.device_type
        index = self.gui.deviceTypeList.findText(device_type, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.gui.deviceTypeList.setCurrentIndex(index)
        self.gui.deviceTypeList.currentIndexChanged.connect(self._device_type_list_changed)

        self.gui.deviceLocationField.setText(self._sensor_data.device_location)
        self.gui.deviceLocationField.textChanged.connect(self._device_location_field_changed)

        self.gui.saveButton.clicked.connect(self._save_button_clicked)
        self.gui.addSensorButton.clicked.connect(self._add_sensor_file_button_clicked)
        self.gui.deleteSensorButton.clicked.connect(self._delete_sensor_file_button_clicked)

        self.gui.sensorDataTree.itemSelectionChanged.connect(self._sensor_selection_changed)
        self._tree_parent_device = QtWidgets.QTreeWidgetItem(self.gui.sensorDataTree)
        self._tree_parent_device.setExpanded(True)
        self._tree_parent_device.setFlags(QtCore.Qt.ItemIsEnabled)
        self._refresh_tree_view()

    def get_title(self):
        """Get window name"""
        title = self._sensor_data.data_id
        return title if not self._has_changes else title + '*'

    @staticmethod
    def get_icon():
        """get icon"""
        return QtGui.QIcon(':/icons/sensor_manager.png')

    def _time_updated(self, time):
        """control current updated slot"""
        self._sensor_data_view_widget.update_central(time)


    def _sensor_selection_changed(self):
        selected_itens = self.gui.sensorDataTree.selectedItems()
        if not selected_itens:
            self.gui.deleteSensorButton.setEnabled(False)
        else:
            self.gui.deleteSensorButton.setEnabled(True)
        self._data_view_refresh()

    def _data_id_field_changed(self, new_data_id):
        self._has_changes = True
        self._sensor_data.data_id = new_data_id
        self.title_updated.emit(self.get_title())
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _device_name_field_changed(self, new_device_name):
        self._has_changes = True
        self._sensor_data.device_name = new_device_name
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _device_type_list_changed(self):
        self._has_changes = True
        self._sensor_data.device_type = self.gui.deviceTypeList.currentText()
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _device_location_field_changed(self, new_location_name):
        self._has_changes = True
        self._sensor_data.device_location = new_location_name
        self._update_tree_view()
        self.title_updated.emit(self.get_title())

    def _save_button_clicked(self):
        """save button clicked signal"""
        self._save()
        self.title_updated.emit(self.get_title())

    def _add_sensor_file_button_clicked(self):
        """add sensor files"""
        sensor_files = utils.get_open_files(self, 'Open Sensor Files', 'Text File (*.txt)')
        for sensor_file in sensor_files:
            sensor_type, data = self._process_sensor_data_file(sensor_file)
            if self._sensor_data.has_sensor(sensor_type.value):
                QtWidgets.QMessageBox.warning(self, "Alert", \
                    "This sensor data already has the {} sensor".format(sensor_type.name),  \
                    QtWidgets.QMessageBox.Ok)
            else:
                self._has_changes = True
                self._sensor_data.add_sensor(sensor_type.value, data)
                self._refresh_tree_view()
                self.title_updated.emit(self.get_title())

    def _delete_sensor_file_button_clicked(self):
        selected_itens = self.gui.sensorDataTree.selectedItems()
        for item in selected_itens:
            self._has_changes = True
            self._sensor_data.remove_sensor(item.text(1))
            self._refresh_tree_view()
            self.title_updated.emit(self.get_title())

    def _data_view_refresh(self):
        selected_itens = self.gui.sensorDataTree.selectedItems()
        if selected_itens:
            selected_sensors = {}
            for selected_item in selected_itens:
                sensor = selected_item.text(1)
                selected_sensors[sensor] = self._sensor_data.sensor_to_list(sensor)
            self._update_time_control(selected_sensors)
            self._time_control_widget.set_enable(True)
            self._time_control_widget.show()
            self._sensor_data_view_widget.show()
            self._sensor_data_view_widget.set_sensor_data('accelerometer', selected_sensors['accelerometer'])
        else:
            self._sensor_data_view_widget.hide()
            self._time_control_widget.set_enable(False)
            self._time_control_widget.hide()

    def _update_time_control(self, selected_sensors):
        """update time control"""
        starts = []
        ends = []
        average_intervals = []
        for data in selected_sensors.values():
            starts.append(data[0][0])
            ends.append(data[-1][0])
            interval = control.utils.time_delta_in_milliseconds(
                data[-1][0], data[0][0]) / float(len(data))
            average_intervals.append(interval)
        start_time = min(starts) if starts else None
        end_time = max(ends) if ends else None
        interval = min(average_intervals) if average_intervals else None
        self._time_control_widget.set_control_values(start_time=start_time,
                                                     end_time=end_time,
                                                     interval=interval)


    def _refresh_tree_view(self):
        # self.gui.sensorDataTree.clear()
        self._update_tree_view()
        self._tree_parent_device.takeChildren()
        for key, value in self._sensor_data.sensors.items():
            child = QtWidgets.QTreeWidgetItem(self._tree_parent_device)
            child.setText(0, '{} ({} values)'.format(str(key), len(value)))
            child.setText(1, str(key))
            child.setIcon(0, QtGui.QIcon(':/icons/sensor.png'))

    def _update_tree_view(self):
        # self.gui.sensorDataTree.clear()
        self._tree_parent_device.setText(0, self._sensor_data.device_name)
        if self._sensor_data.device_type == 'smartphone':
            self._tree_parent_device.setIcon(0, QtGui.QIcon(':/icons/smartphone.png'))
        if self._sensor_data.device_type == 'smartwatch':
            self._tree_parent_device.setIcon(0, QtGui.QIcon(':/icons/smartwatch.png'))


    @staticmethod
    def _process_sensor_data_file(sensor_data_file):
        """process a text file with sensor data"""
        data = []
        sensor_type = None
        for s_type in SensorType:
            if s_type.value in sensor_data_file:
                sensor_type = s_type
        if sensor_type is not None:
            for line in open(sensor_data_file):
                splited_line = line.split(';')
                if sensor_type.value in ('accelerometer', 'gyroscope', 'magnetometer'):
                    if len(splited_line) == 4:
                        timestamp, x_value, y_value, z_value = splited_line
                        timestamp = dateutil.parser.parse(timestamp)
                        data.append({
                            'values':{'x':float(x_value.replace(',', '.')),
                                      'y':float(y_value.replace(',', '.')),
                                      'z':float(z_value.replace(',', '.'))},
                            'timestamp': timestamp
                            })
                elif sensor_type.value == 'barometer':
                    if len(splited_line) == 2:
                        timestamp, hpa = splited_line
                        timestamp = dateutil.parser.parse(timestamp)
                        data.append({
                            'values':{'hpa':float(hpa.replace(',', '.'))},
                            'timestamp': timestamp
                        })
                elif sensor_type.value == 'gps':
                    if len(splited_line) == 3:
                        timestamp, latitude, longitude = splited_line
                        timestamp = dateutil.parser.parse(timestamp)
                        data.append({
                            'values':{'latitude':float(latitude.replace(',', '.')),
                                      'longitude':float(longitude.replace(',', '.'))},
                            'timestamp': timestamp
                            })
        return sensor_type, data


    def _save(self):
        if self._sensor_data.sensors_count == 0:
            confirm_save = QtWidgets.QMessageBox.warning(self, "Alert", \
                "This data does not have any sensor. Do you want save?",  \
                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
            if confirm_save == QtWidgets.QMessageBox.Cancel:
                return False

        if self._sensor_data.json_file is not None:
            self._sensor_data.save()
            self._has_changes = False
        else:
            suggestion = os.path.join(self._working_dir, self._sensor_data.data_id + '.json')
            json_file = utils.get_save_file(self, 'Save file', "JSON Files (*.json)", suggestion)
            if json_file is None:
                return False
            self._sensor_data.save(json_file)
            self._has_changes = False
        return True

    def closeEvent(self, event):
        """close event"""
        if not self._has_changes:
            event.accept()
        else:
            save_question = utils.save_message_box(self)
            if save_question == QtWidgets.QMessageBox.Save:
                if self._save():
                    event.accept()
                else:
                    event.ignore()
            elif save_question == QtWidgets.QMessageBox.Cancel:
                event.ignore()
            elif save_question == QtWidgets.QMessageBox.Discard:
                event.accept()
