"""SensorSetManagerMDI class file."""

# import os
# import dateutil.parser
#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QTreeWidgetItem#, QMessageBox
from PyQt5.QtCore import Qt
from gui.base_mdi import BaseMDI
from gui.ui import VisualSensorDataViewMDIUi
from gui.sensor_data_view_widget import SensorDataViewWidget
from gui.visual_data_view_widget import VisualDataViewWidget
from gui.time_control_widget import TimeControlWidget
from gui.gui_utils import get_open_file
from gui.plot.plot_data import PlotData
from models import SensorSetData, VisualData
# from models.sensor_data import SENSORTYPES, SENSORTYPES_VALUES_SIZES
#pylint: enable=E0401
#pylint: enable=E0611

class VisualSensorDataViewMDI(BaseMDI):
    """Main Window class"""

    ###############################################################################################
    # Init Method
    ###############################################################################################
    def __init__(self, parent=None):
        """Init method"""
        BaseMDI.__init__(self, parent, VisualSensorDataViewMDIUi)

        self._working_dir = None
        self._has_changes = None
        self._sensor_data_view_widget = None
        self._visual_data_view_widget = None
        self._time_control_widget = None

        self._tree_parent_visual = None
        self._tree_parent_sensor = None

        self._sensors_set_data = {}
        self._visuals_data = {}

        self._current_visual_data = None

        self._configure_gui()
        self._make_connections()

    ###############################################################################################
    # Public Methods
    ###############################################################################################
    @staticmethod
    def get_title():
        """Get window name"""
        return 'VisualSensor Data View'

    @staticmethod
    def get_icon():
        """get icon"""
        return QIcon(':/icons/data_view.png')

    ###############################################################################################
    # Private Methods
    ###############################################################################################
    def _configure_gui(self):
        self.gui.verticalSplitter.setStretchFactor(0, 3)
        self.gui.verticalSplitter.setStretchFactor(1, 10)
        self.gui.horizontalSplitter.setStretchFactor(0, 1)
        self.gui.horizontalSplitter.setStretchFactor(1, 20)

        self._sensor_data_view_widget = SensorDataViewWidget()
        self._visual_data_view_widget = VisualDataViewWidget()
        self._time_control_widget = TimeControlWidget()
        layout = QVBoxLayout()
        layout.addWidget(self._visual_data_view_widget)
        layout.addWidget(self._time_control_widget)
        self.gui.visualDataViewGroup.setLayout(layout)

        layout = QVBoxLayout()
        layout.addWidget(self._sensor_data_view_widget)
        self.gui.sensorDataViewGroup.setLayout(layout)

        self._tree_parent_visual = QTreeWidgetItem(self.gui.dataTree)
        self._tree_parent_visual.setExpanded(True)
        self._tree_parent_visual.setFlags(Qt.ItemIsEnabled)
        self._tree_parent_sensor = QTreeWidgetItem(self.gui.dataTree)
        self._tree_parent_sensor.setExpanded(True)
        self._tree_parent_sensor.setFlags(Qt.ItemIsEnabled)
        self._refresh_tree_view()
        #
        # self._data_view_refresh()

    def _make_connections(self):
        self.gui.addSensorSetDataButton.clicked.connect(self._add_sensor_data_button_clicked)
        self.gui.addVisualDataButton.clicked.connect(self._add_visual_data_button_clicked)
        self.gui.dataTree.itemSelectionChanged.connect(self._data_tree_selection_changed)
        self._time_control_widget.time_updated.connect(self._time_updated)

    def _update_tree_view(self):
        self._tree_parent_sensor.setText(0, 'Sensor Data')
        self._tree_parent_visual.setIcon(0, QIcon(':/icons/visual_manager.png'))
        self._tree_parent_visual.setText(0, 'Visual Data')
        self._tree_parent_sensor.setIcon(0, QIcon(':/icons/sensor_manager.png'))

    def _refresh_tree_view(self):
        self._update_tree_view()
        self._tree_parent_visual.takeChildren()
        self._tree_parent_sensor.takeChildren()

        for sensor_set_data in self._sensors_set_data.values():
            devicechild = QTreeWidgetItem(self._tree_parent_sensor)
            devicechild.setText(0, sensor_set_data.data_id)
            devicechild.setExpanded(True)
            devicechild.setFlags(Qt.ItemIsEnabled)
            if sensor_set_data.device_type == 'smartphone':
                devicechild.setIcon(0, QIcon(':/icons/smartphone.png'))
            elif sensor_set_data.device_type == 'smartwatch':
                devicechild.setIcon(0, QIcon(':/icons/smartwatch.png'))
            for sensor_data in sensor_set_data.sensors_data:
                child = QTreeWidgetItem(devicechild)
                child_text = '{} ({} values)'.format(sensor_data.sensor_type,
                                                     len(sensor_data.readings))
                child.setText(0, child_text)
                child.setText(1, 'sensordata')
                child.setText(2, sensor_set_data.data_id)
                child.setText(3, sensor_data.sensor_type)
                child.setIcon(0, QIcon(':/icons/sensor.png'))

        for visual_data in self._visuals_data.values():
            visualchild = QTreeWidgetItem(self._tree_parent_visual)
            visualchild.setExpanded(True)
            visualchild.setIcon(0, QIcon(':/icons/visual.png'))
            visualchild.setText(0, visual_data.data_id)
            visualchild.setText(1, 'visualdata')

    def _data_view_refresh(self):
        selected_itens = self.gui.dataTree.selectedItems()
        if selected_itens:
            selected_plots_data = []
            selected_visuals_data = []
            selected_temporals_data = []
            for selected_item in selected_itens:
                selected_type = selected_item.text(1)
                if selected_type == 'sensordata':
                    sensor_set_data = self._sensors_set_data[selected_item.text(2)]
                    sensor_type = selected_item.text(3)
                    sensor_data = sensor_set_data.get_sensor_data(sensor_type)
                    plot_data = self._make_plot_data(sensor_data)
                    if plot_data is not None:
                        selected_temporals_data.append(sensor_data)
                        selected_plots_data.append(plot_data)
                if selected_type == 'visualdata':
                    visual_data = self._visuals_data[selected_item.text(0)]
                    selected_temporals_data.append(visual_data)
                    selected_visuals_data.append(visual_data)
            if selected_temporals_data:
                start_time, _ = self._update_time_control(selected_temporals_data)
                self._time_control_widget.set_enable(True)
                self._time_control_widget.show()
            if selected_plots_data:
                self._sensor_data_view_widget.clear()
                self._sensor_data_view_widget.add_plots_data(selected_plots_data)
                self._sensor_data_view_widget.update_central_time(start_time)
                self._sensor_data_view_widget.show()
            if selected_visuals_data:
                self._current_visual_data = selected_visuals_data[0]
                self._visual_data_view_widget.show()
        else:
            self._sensor_data_view_widget.hide()
            self._visual_data_view_widget.hide()
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
        return start_time, end_time

    ###############################################################################################
    # Private Slots
    ###############################################################################################
    def _add_sensor_data_button_clicked(self):
        sensor_data_file = get_open_file(self, 'Open Sensor Data', 'JSON File (*.json)')
        if sensor_data_file is not None:
            sensor_set_data = SensorSetData(sensor_data_file)
            self._sensors_set_data[sensor_set_data.data_id] = sensor_set_data
            self._refresh_tree_view()

    def _add_visual_data_button_clicked(self):
        visual_data_file = get_open_file(self, 'Open Visual Data', 'JSON File (*.json)')
        if visual_data_file is not None:
            visual_data = VisualData(visual_data_file)
            self._visuals_data[visual_data.data_id] = visual_data
            self._refresh_tree_view()

    def _data_tree_selection_changed(self):
        self._data_view_refresh()

    def _time_updated(self, time):
        """control current updated slot"""
        self._sensor_data_view_widget.update_central_time(time)
        if self._current_visual_data:
            frame, _ = self._current_visual_data.frame_at_time(time)
            if frame is not None:
                self._visual_data_view_widget.update_frame(frame)



    ###############################################################################################
    # Protected auxiliar method
    ###############################################################################################
    # def _process_sensor_data_file(self, sensor_data_file):
    #     """process a text file with sensor data"""
    #
    #     if not os.path.isfile(sensor_data_file):
    #         QMessageBox.critical(self, 'Error', 'File not found: {}', QMessageBox.Ok)
    #
    #     sensor_type = None
    #     for s_type in SENSORTYPES:
    #         if s_type in sensor_data_file:
    #             sensor_type = s_type
    #
    #     if sensor_type is None:
    #         QMessageBox.critical(self, 'Error', 'Invalid sensor type: {}', QMessageBox.Ok)
    #         return None, None
    #
    #     readings = []
    #     for line in open(sensor_data_file):
    #         reading = line.split(';')
    #         if len(reading) != (SENSORTYPES_VALUES_SIZES[sensor_type] + 1):
    #             QMessageBox.critical(self, 'Error', 'Invalid sensor type: {}', QMessageBox.Ok)
    #             return None, None
    #         reading[0] = dateutil.parser.parse(reading[0])
    #         for idx in range(1, len(reading)):
    #             reading[idx] = float(reading[idx].replace(',', '.'))
    #         readings.append(reading)
    #
    #     return sensor_type, readings

    ###############################################################################################
    # Override methods
    ###############################################################################################
    #pylint: disable=C0103
    # def closeEvent(self, event):
    #     """close event"""
    #     if not self._has_changes:
    #         event.accept()
    #     else:
    #         save_question = save_message_box(self)
    #         if save_question == QMessageBox.Save:
    #             if self._save():
    #                 event.accept()
    #             else:
    #                 event.ignore()
    #         elif save_question == QMessageBox.Cancel:
    #             event.ignore()
    #         elif save_question == QMessageBox.Discard:
    #             event.accept()
    #pylint: enable=C0103
