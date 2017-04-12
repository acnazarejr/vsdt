#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
#pylint: disable=R0903
"""Main Window class"""

import os
import dateutil
from PyQt5 import QtWidgets

from gui.ui import VisualDataManagerWindowUi
from gui.control_widget import ControlWidget
from gui.visual_data_form import VisualDataForm
from gui.utils import open_visual_data

class VisualDataManagerWindow(QtWidgets.QMainWindow):
    """Main Window class"""

    def __init__(self, parent=None):
        """Init method"""
        QtWidgets.QMainWindow.__init__(self, parent)
        self.gui = VisualDataManagerWindowUi()
        self.gui.setupUi(self)

        self._visual_data = None

        self._visual_data_form = VisualDataForm()
        self._control_widget = ControlWidget()
        self.gui.framesViewGroupVerticalLayout.addWidget(self._visual_data_form)
        self.gui.framesViewGroupVerticalLayout.addWidget(self._control_widget)

        self.gui.openVideoButton.clicked.connect(self._open_video_button_clicked)
        self.gui.syncButton.clicked.connect(self._sync_button_clicked)
        self.gui.exportButton.clicked.connect(self._export_button_clicked)
        self.gui.importButton.clicked.connect(self._import_button_clicked)
        self._control_widget.time_updated.connect(self._visual_data_updated)

        # reg = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{0,6}'
        # validator = QtGui.QRegExpValidator(QtCore.QRegExp(reg))
        # self.gui.currentTimestampField.setValidator(validator)

        self._sync_options_enable(False)

    def _open_video_button_clicked(self):
        """Open video button clicked signal"""
        self._visual_data = open_visual_data(self)
        if self._visual_data is not None:
            self.gui.videoFileField.setText(self._visual_data.video_file)
            self._control_widget.set_control_values(start_time=self._visual_data.start_time,
                                                    end_time=self._visual_data.end_time,
                                                    interval=self._visual_data.interval)
            self._control_widget.set_enable(True)
            self._sync_options_enable(True)

    def _sync_button_clicked(self):
        """Symc button clicked signal"""
        str_timestamp = self.gui.currentTimestampField.text()
        timestamp = dateutil.parser.parse(str_timestamp)
        self._visual_data.synchonize_timestamps(timestamp)
        self._control_widget.set_control_values(start_time=self._visual_data.start_time,
                                                end_time=self._visual_data.end_time,
                                                interval=self._visual_data.interval)

    def _export_button_clicked(self):
        """Export button clicked signal"""

        suggest_file = os.path.splitext(self._visual_data.video_file)[0] + '.json'
        json_file_name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', suggest_file,
                                                               "JSON Files (*.json)")

        if json_file_name[0] != '':
            self._visual_data.save_json(json_file_name[0])

    def _import_button_clicked(self):
        """Export button clicked signal"""

        suggest_file = os.path.splitext(self._visual_data.video_file)[0] + '.json'
        json_file_name = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', suggest_file,
                                                               "JSON Files (*.json)")

        if json_file_name[0] != '':
            self._visual_data.load_json(json_file_name[0])
            self._control_widget.set_control_values(start_time=self._visual_data.start_time,
                                                    end_time=self._visual_data.end_time,
                                                    interval=self._visual_data.interval)

    def _visual_data_updated(self, time):
        """control current updated slot"""
        frame, timestamp = self._visual_data.get_frame(time)
        self.gui.currentTimestampField.setText(timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self._visual_data_form.update_frame(frame)

    def _sync_options_enable(self, value):
        """enable or disabel sync options"""
        self.gui.currentTimestampField.setEnabled(value)
        self.gui.currentTimestampLabel.setEnabled(value)
        self.gui.exportButton.setEnabled(value)
        self.gui.importButton.setEnabled(value)
        self.gui.syncButton.setEnabled(value)
