#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
#pylint: disable=R0903
"""Main Window class"""

import os
import dateutil
from PyQt5 import QtWidgets
from gui.ui import VisualDataManagerMDIWidgetUi
from gui.time_control_widget import TimeControlWidget
from gui.visual_data_view_widget import VisualDataViewWidget
from gui.base_mdi_widget import BaseMDIWidget
from models import VisualData

class VisualDataManagerMDIWidget(BaseMDIWidget):
    """Main Window class"""

    def __init__(self, visual_data=None, parent=None):
        """Init method"""
        BaseMDIWidget.__init__(self, parent, VisualDataManagerMDIWidgetUi)

        if visual_data is None:
            self._visual_data = VisualData()
            self._has_changes = True
        else:
            self._visual_data = visual_data

        self._visual_data_view_widget = VisualDataViewWidget()
        self._time_control_widget = TimeControlWidget()
        self.gui.framesViewGroupVerticalLayout.addWidget(self._visual_data_view_widget)
        self.gui.framesViewGroupVerticalLayout.addWidget(self._time_control_widget)

        data_id = self._visual_data if self._visual_data.data_id is not None else "new_visual_data"
        self.gui.dataIDField.setText(data_id)
        self.gui.dataIDField.textChanged.connect(self._data_id_field_changed)

        # self.gui.openVideoButton.clicked.connect(self._open_video_button_clicked)
        # self.gui.syncButton.clicked.connect(self._sync_button_clicked)
        # self.gui.exportButton.clicked.connect(self._export_button_clicked)
        # self.gui.importButton.clicked.connect(self._import_button_clicked)
        # self._control_widget.time_updated.connect(self._visual_data_updated)

        # reg = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{0,6}'
        # validator = QtGui.QRegExpValidator(QtCore.QRegExp(reg))
        # self.gui.currentTimestampField.setValidator(validator)

        self._sync_options_enable(False)

    def get_title(self):
        """Get window name"""
        title = self.gui.dataIDField.text()
        return title if not self._has_changes else title + '*'

    def _data_id_field_changed(self, _):
        self._has_changes = True
        self.title_updated.emit(self.get_title())

    # def _open_video_button_clicked(self):
    #     """Open video button clicked signal"""
    #     self._visual_data = open_visual_data(self)
    #     if self._visual_data is not None:
    #         self.gui.videoFileField.setText(self._visual_data.video_file)
    #         self._control_widget.set_control_values(start_time=self._visual_data.start_time,
    #                                                 end_time=self._visual_data.end_time,
    #                                                 interval=self._visual_data.interval)
    #         self._control_widget.set_enable(True)
    #         self._sync_options_enable(True)
    #
    # def _sync_button_clicked(self):
    #     """Symc button clicked signal"""
    #     str_timestamp = self.gui.currentTimestampField.text()
    #     timestamp = dateutil.parser.parse(str_timestamp)
    #     self._visual_data.synchonize_timestamps(timestamp)
    #     self._control_widget.set_control_values(start_time=self._visual_data.start_time,
    #                                             end_time=self._visual_data.end_time,
    #                                             interval=self._visual_data.interval)
    #
    # def _export_button_clicked(self):
    #     """Export button clicked signal"""
    #
    #     suggest_file = os.path.splitext(self._visual_data.video_file)[0] + '.json'
    #     json_file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', suggest_file,
    #                                                            "JSON Files (*.json)")
    #
    #     if json_file_name[0] != '':
    #         self._visual_data.save_json(json_file_name[0])
    #
    # def _import_button_clicked(self):
    #     """Export button clicked signal"""
    #
    #     suggest_file = os.path.splitext(self._visual_data.video_file)[0] + '.json'
    #     json_file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', suggest_file,
    #                                                            "JSON Files (*.json)")
    #
    #     if json_file_name[0] != '':
    #         self._visual_data.load_json(json_file_name[0])
    #         self._control_widget.set_control_values(start_time=self._visual_data.start_time,
    #                                                 end_time=self._visual_data.end_time,
    #                                                 interval=self._visual_data.interval)
    #
    # def _visual_data_updated(self, time):
    #     """control current updated slot"""
    #     frame, timestamp = self._visual_data.get_frame(time)
    #     self.gui.currentTimestampField.setText(timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"))
    #     self._visual_data_form.update_frame(frame)
    #
    def _sync_options_enable(self, value):
        """enable or disabel sync options"""
        # self.gui.currentTimestampField.setEnabled(value)
        # self.gui.currentTimestampLabel.setEnabled(value)
        # self.gui.exportButton.setEnabled(value)
        # self.gui.importButton.setEnabled(value)
        # self.gui.syncButton.setEnabled(value)
