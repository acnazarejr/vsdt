"""VisualManagerMDI class file."""

import os
import dateutil.parser
#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox
from PyQt5.QtCore import QRegExp
from gui.base_mdi import BaseMDI
from gui.ui import VisualManagerMDIUi
from gui.visual_data_view_widget import VisualDataViewWidget
from gui.time_control_widget import TimeControlWidget
from gui.gui_utils import get_save_file, save_message_box
#pylint: enable=E0401
#pylint: enable=E0611

class VisualManagerMDI(BaseMDI):
    """VisualManagerMDI class."""

    ###############################################################################################
    # Init Method
    ###############################################################################################
    def __init__(self, visual_data, working_dir=None, has_changes=False, parent=None):
        """Init method."""
        BaseMDI.__init__(self, parent, VisualManagerMDIUi)

        self._visual_data = visual_data
        self._working_dir = working_dir
        self._has_changes = has_changes
        self._visual_data_view_widget = None
        self._time_control_widget = None
        self._json_file = None

        self._configure_gui()
        self._fill_fields()
        self._make_connections()

        self._time_control_widget.set_control_values(start_time=self._visual_data.start_time,
                                                     end_time=self._visual_data.end_time,
                                                     interval=self._visual_data.interval)
        self._time_control_widget.set_enable(True)

    ###############################################################################################
    # Public Methods
    ###############################################################################################
    def get_title(self):
        """Get window title."""
        title = self._visual_data.data_id
        return title if not self._has_changes else title + '*'

    @staticmethod
    def get_icon():
        """Get window icon."""
        return QIcon(':/icons/visual_manager.png')

    def set_json_file(self, json_file):
        """Set json file."""
        self._json_file = json_file

    ###############################################################################################
    # Private Methods
    ###############################################################################################
    def _configure_gui(self):
        """Configure GUI."""
        self._visual_data_view_widget = VisualDataViewWidget()
        self._time_control_widget = TimeControlWidget()
        layout = QVBoxLayout()
        layout.addWidget(self._visual_data_view_widget)
        layout.addWidget(self._time_control_widget)
        self.gui.dataVisualizationGroup.setLayout(layout)
        reg = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}.[0-9]{0,6}'
        validator = QRegExpValidator(QRegExp(reg))
        self.gui.currentTimestampField.setValidator(validator)

    def _fill_fields(self):
        """Fill GUI fields"""
        self.gui.dataIDField.setText(self._visual_data.data_id)

    def _make_connections(self):
        """Make signals and slots connections"""
        self.gui.dataIDField.textChanged.connect(self._data_id_field_changed)
        self.gui.syncButton.clicked.connect(self._sync_button_clicked)
        self.gui.saveButton.clicked.connect(self._save_button_clicked)
        self._time_control_widget.time_updated.connect(self._time_updated)

    def _save(self):
        if self._json_file is not None:
            self._visual_data.save(self._json_file)
            self._has_changes = False
        else:
            suggestion = os.path.join(self._working_dir, self._visual_data.data_id + '.json')
            json_file = get_save_file(self, 'Save file', "JSON Files (*.json)", suggestion)
            if json_file is None:
                return False
            self._visual_data.save(json_file)
            self._json_file = json_file
            self._has_changes = False
        return True

    ###############################################################################################
    # Private Slots
    ###############################################################################################
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
        frame, timestamp = self._visual_data.frame_at_time(time)
        self.gui.currentTimestampField.setText(timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f"))
        self._visual_data_view_widget.update_frame(frame)

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
