#pylint: disable=R0201
"""VSDT main app file."""

import os
import sys
from PyQt5 import QtWidgets
from models import VisualData
from gui.ui import MainWindowUiBase, MainWindowUi
from gui.visual_manager_mdi import VisualManagerMDI
from gui.mdi_sub_window import MDISubWindow
from gui.gui_utils import get_open_file

class VSDT(MainWindowUiBase):
    """VSDT Main class."""

    def __init__(self):
        #pylint: disable=E1101
        QtWidgets.QMainWindow.__init__(self, None)
        #pylint: enable=E1101
        self.gui = MainWindowUi()
        self.gui.setupUi(self)

        self._make_connections()


        # #self._video_control = VideoControl(Raspicam(640, 480, 15))
        #
        # self._visual_data_form = self._create_visual_data_form()
        # self._control_form = self._create_control_form()
        # self._sensor_data_form = self._create_sensor_data_form()
        #
        # self.gui.splitter.addWidget(self._visual_data_form)
        # self.gui.splitter.addWidget(self._control_form)
        # self.gui.splitter.addWidget(self._sensor_data_form)
        #
        # self.gui.visualSensorRadioButton.clicked.connect(self._operation_mode_clicked)
        # self.gui.visualRadioButton.clicked.connect(self._operation_mode_clicked)
        # self.gui.sensorRadioButton.clicked.connect(self._operation_mode_clicked)
        #
        # self.gui.openVideoButton.clicked.connect(self._open_video_button_clicked)
        #
        # self._control_form.visual_data_updated.connect(self._visual_data_updated)
        # self._control_form.sensor_data_updated.connect(self._sensor_data_updated)

    def _make_connections(self):
        """Connect menu bar actions"""
        self.gui.newVisualDataAction.triggered.connect(self._new_visual_data_action)
        self.gui.openVisualDataAction.triggered.connect(self._open_visual_data_action)
        # self.gui.newSensorDataAction.triggered.connect(self._new_sensor_data_action)
        # self.gui.openSensorDataAction.triggered.connect(self._open_sensor_data_action)

    def _new_visual_data_action(self):
        """New visual data action"""
        video_file = get_open_file(self, 'Open Video File', 'Video files (*.mp4 *.avi)')
        if video_file is not None:
            working_dir = os.path.dirname(video_file)
            visual_data = VisualData.create_from_video(video_file)
            visual_data_manager_mdi_widget = VisualManagerMDI(
                visual_data, working_dir=working_dir, has_changes=True)
            self._open_sub_window(visual_data_manager_mdi_widget)

    def _open_visual_data_action(self):
        """New visual data action"""
        visual_data_file = get_open_file(self, 'Open Visual Data', 'JSON File (*.json)')
        if visual_data_file is not None:
            working_dir = os.path.dirname(visual_data_file)
            visual_data = VisualData(visual_data_file)
            visual_data_manager_mdi_widget = VisualManagerMDI(
                visual_data, working_dir=working_dir, has_changes=False)
            self._open_sub_window(visual_data_manager_mdi_widget)

#     def _new_sensor_data_action(self):
#         """New visual data action"""
#         sensor_data = SensorData()
#         sensor_data.data_id = 'new_sensor_data'
#         settings = utils.get_settings()
#         working_dir = settings.value('last_dir', type=str)
#         sensor_data_manager_mdi_widget = SensorDataManagerMDIWidget(
#             sensor_data, working_dir=working_dir, has_changes=True)
#         self._open_sub_window(sensor_data_manager_mdi_widget)
#
#     def _open_sensor_data_action(self):
#         """New visual data action"""
#         sensor_data_file = utils.get_open_file(self, 'Open Sensor Data', 'JSON File (*.json)')
#         if sensor_data_file is not None:
#             working_dir = os.path.dirname(sensor_data_file)
#             sensor_data = SensorData(sensor_data_file)
#             sensor_data_manager_mdi_widget = SensorDataManagerMDIWidget(
#                 sensor_data, working_dir=working_dir, has_changes=False)
#             self._open_sub_window(sensor_data_manager_mdi_widget)
#
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
    window.show()
    sys.exit(app.exec_())
    #pylint: enable=E1101

if __name__ == '__main__':
    run()
