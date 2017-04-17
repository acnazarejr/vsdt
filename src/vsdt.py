#pylint: disable=R0201
"""VSDT main app file."""

import os
import sys
from PyQt5 import QtWidgets
from models import VisualData, SensorSetData
from gui.ui import MainWindowUiBase, MainWindowUi
from gui.visual_manager_mdi import VisualManagerMDI
from gui.sensor_set_manager_mdi import SensorSetManagerMDI
from gui.mdi_sub_window import MDISubWindow
from gui.gui_utils import get_open_file, get_settings

#pylint: disable=R0903
class VSDT(MainWindowUiBase):
    """VSDT Main class."""

    def __init__(self):
        #pylint: disable=E1101
        QtWidgets.QMainWindow.__init__(self, None)
        #pylint: enable=E1101
        self.gui = MainWindowUi()
        self.gui.setupUi(self)

        self._make_connections()

    def _make_connections(self):
        """Connect menu bar actions"""
        self.gui.newVisualDataAction.triggered.connect(self._new_visual_data_action)
        self.gui.openVisualDataAction.triggered.connect(self._open_visual_data_action)
        self.gui.newSensorDataAction.triggered.connect(self._new_sensor_data_action)
        self.gui.openSensorDataAction.triggered.connect(self._open_sensor_data_action)

    def _new_visual_data_action(self):
        """New visual data action"""
        video_file = get_open_file(self, 'Open Video File', 'Video files (*.mp4 *.avi)')
        if video_file is not None:
            working_dir = os.path.dirname(video_file)
            visual_data = VisualData.create_from_video(video_file)
            visual_manager_mdi = VisualManagerMDI(
                visual_data, working_dir=working_dir, has_changes=True)
            self._open_sub_window(visual_manager_mdi)

    def _open_visual_data_action(self):
        """New visual data action"""
        visual_data_file = get_open_file(self, 'Open Visual Data', 'JSON File (*.json)')
        if visual_data_file is not None:
            working_dir = os.path.dirname(visual_data_file)
            visual_data = VisualData(visual_data_file)
            visual_manager_mdi = VisualManagerMDI(
                visual_data, working_dir=working_dir, has_changes=False)
            visual_manager_mdi.set_json_file(visual_data_file)
            self._open_sub_window(visual_manager_mdi)

    def _new_sensor_data_action(self):
        """New visual data action"""
        sensor_set_data = SensorSetData()
        sensor_set_data.data_id = 'new_sensor_data'
        settings = get_settings()
        working_dir = settings.value('last_dir', type=str)
        sensor_set_manager_mdi = SensorSetManagerMDI(
            sensor_set_data, working_dir=working_dir, has_changes=True)
        self._open_sub_window(sensor_set_manager_mdi)

    def _open_sensor_data_action(self):
        """New visual data action"""
        sensor_data_file = get_open_file(self, 'Open Sensor Data', 'JSON File (*.json)')
        if sensor_data_file is not None:
            working_dir = os.path.dirname(sensor_data_file)
            sensor_data = SensorSetData(sensor_data_file)
            sensor_set_manager_mdi = SensorSetManagerMDI(
                sensor_data, working_dir=working_dir, has_changes=False)
            sensor_set_manager_mdi.set_json_file(sensor_data_file)
            self._open_sub_window(sensor_set_manager_mdi)

    def _open_sub_window(self, widget):
        """Open a new MDI SubWindow"""
        sub = MDISubWindow()
        sub.setWidget(widget)
        self.gui.mdiArea.addSubWindow(sub)
        sub.show()

def run():
    """ Start the GUI."""
    #pylint: disable=E1101
    app = QtWidgets.QApplication(sys.argv)
    window = VSDT()
    window.showMaximized()
    sys.exit(app.exec_())
    #pylint: enable=E1101

if __name__ == '__main__':
    run()
