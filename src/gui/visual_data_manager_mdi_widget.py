#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
#pylint: disable=R0903
"""Main Window class"""

import os
import dateutil.parser
from PyQt5 import QtGui, QtCore, QtWidgets
from gui import utils
from gui.ui import VisualDataManagerMDIWidgetUi
from gui.time_control_widget import TimeControlWidget
from gui.visual_data_view_widget import VisualDataViewWidget
from gui.base_mdi_widget import BaseMDIWidget

class VisualDataManagerMDIWidget(BaseMDIWidget):
    """Main Window class"""

    def __init__(self, visual_data, working_dir=None, has_changes=False, parent=None):
        """Init method"""
        BaseMDIWidget.__init__(self, parent, VisualDataManagerMDIWidgetUi)

        self._visual_data = visual_data
        self._working_dir = working_dir
        self._has_changes = has_changes

        self._visual_data_view_widget = VisualDataViewWidget()
        self._time_control_widget = TimeControlWidget()
        self.gui.dataVisualizationGroupVerticalLayout.addWidget(self._visual_data_view_widget)
        self.gui.dataVisualizationGroupVerticalLayout.addWidget(self._time_control_widget)

        self.gui.dataIDField.setText(self._visual_data.data_id)
        self.gui.dataIDField.textChanged.connect(self._data_id_field_changed)

        self.gui.syncButton.clicked.connect(self._sync_button_clicked)
        self.gui.saveButton.clicked.connect(self._save_button_clicked)
        self._time_control_widget.time_updated.connect(self._time_updated)

        self._time_control_widget.set_control_values(start_time=self._visual_data.start_time,
                                                     end_time=self._visual_data.end_time,
                                                     interval=self._visual_data.interval)
        self._time_control_widget.set_enable(True)

        reg = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{0,6}'
        validator = QtGui.QRegExpValidator(QtCore.QRegExp(reg))
        self.gui.currentTimestampField.setValidator(validator)

    def get_title(self):
        """Get window name"""
        title = self._visual_data.data_id
        return title if not self._has_changes else title + '*'

    @staticmethod
    def get_icon():
        """get icon"""
        return QtGui.QIcon(':/icons/visual_manager.png')

    def _data_id_field_changed(self, new_data_id):
        self._has_changes = True
        self._visual_data.data_id = new_data_id
        self.title_updated.emit(self.get_title())

    def _sync_button_clicked(self):
        """Symc button clicked signal"""
        self._has_changes = True
        str_timestamp = self.gui.currentTimestampField.text()
        timestamp = dateutil.parser.parse(str_timestamp)
        self._visual_data.synchonize_timestamps(timestamp)
        self._time_control_widget.set_control_values(start_time=self._visual_data.start_time,
                                                     end_time=self._visual_data.end_time,
                                                     interval=self._visual_data.interval)
        self.title_updated.emit(self.get_title())

    def _save_button_clicked(self):
        """save button clicked signal"""
        self._save()
        self.title_updated.emit(self.get_title())

    def _time_updated(self, time):
        """control current updated slot"""
        frame, timestamp = self._visual_data.get_frame(time)
        self.gui.currentTimestampField.setText(timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self._visual_data_view_widget.update_frame(frame)

    def _save(self):
        if self._visual_data.json_file is not None:
            self._visual_data.save()
            self._has_changes = False
        else:
            suggestion = os.path.join(self._working_dir, self._visual_data.data_id + '.json')
            json_file = utils.get_save_file(self, 'Save file', "JSON Files (*.json)", suggestion)
            if json_file is None:
                return False
            self._visual_data.save(json_file)
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
