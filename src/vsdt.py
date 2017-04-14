#pylint: disable=R0201
#pylint: disable=R0903
"""Main app file"""

import os
import sys

from PyQt5 import QtWidgets

from gui.ui import MainWindowUiBase, MainWindowUi
from gui import VisualDataManagerMDIWidget
from gui import MDISubWindow
from gui import utils
from models import VisualData


class VSDT(MainWindowUiBase):
    """Biobox main class"""

    def __init__(self):
        #pylint: disable=E1101
        QtWidgets.QMainWindow.__init__(self, None)
        #pylint: enable=E1101
        self.gui = MainWindowUi()
        self.gui.setupUi(self)

        # self._visual_data_manager_window = VisualDataManagerWindow()
        # self._sensor_data_manager_window = SensorDataManagerWindow()

        self._connect_actions()


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

    def _connect_actions(self):
        """Connect menu bar actions"""
        self.gui.newVisualDataAction.triggered.connect(self._new_visual_data_action)
        self.gui.openVisualDataAction.triggered.connect(self._open_visual_data_action)


    def _new_visual_data_action(self):
        """New visual data action"""
        video_file = utils.get_open_file(self, 'Open Video File', 'Video files (*.mp4 *.avi)')
        if video_file is not None:
            working_dir = os.path.dirname(video_file)
            visual_data = VisualData.create_from_video(video_file)
            visual_data_manager_mdi_widget = VisualDataManagerMDIWidget(
                visual_data, working_dir=working_dir, has_changes=True)
            self._open_sub_window(visual_data_manager_mdi_widget)

    def _open_visual_data_action(self):
        """New visual data action"""
        visual_data_file = utils.get_open_file(self, 'Open Visual Data', 'JSON File (*.json)')
        if visual_data_file is not None:
            working_dir = os.path.dirname(visual_data_file)
            visual_data = VisualData(visual_data_file)
            visual_data_manager_mdi_widget = VisualDataManagerMDIWidget(
                visual_data, working_dir=working_dir, has_changes=False)
            self._open_sub_window(visual_data_manager_mdi_widget)

    def _open_sub_window(self, widget):
        """Open a new MDI SubWindow"""
        sub = MDISubWindow()
        sub.setWidget(widget)
        self.gui.mdiArea.addSubWindow(sub)
        sub.show()

    # def _create_visual_data_form(self):
    #     """create visual data form"""
    #     form = VisualDataForm()
    #     return form
    #
    # def _create_sensor_data_form(self):
    #     """create visual data form"""
    #     form = SensorDataForm()
    #     form.set_sensor_data(SensorData(""))
    #     return form
    #
    # def _create_control_form(self):
    #     """create control form"""
    #     form = ControlForm()
    #     return form
    #
    # def _operation_mode_clicked(self):
    #     """ """
    #     self.gui.openVideoButton.setEnabled(False)
    #     self.gui.openSensorButton.setEnabled(False)
    #
    #     mode = self._checked_operation_mode()
    #     if mode == 'visualSensorRadioButton':
    #         self.gui.openVideoButton.setEnabled(True)
    #         self.gui.openSensorButton.setEnabled(False)
    #     elif mode == 'visualRadioButton':
    #         self.gui.openVideoButton.setEnabled(True)
    #     elif mode == 'sensorRadioButton':
    #         self.gui.openSensorButton.setEnabled(False)
    #
    # def _checked_operation_mode(self):
    #     """returns the operation mode checked"""
    #     radios = [self.gui.visualSensorRadioButton,
    #               self.gui.visualRadioButton,
    #               self.gui.sensorRadioButton]
    #
    #     for radio in radios:
    #         if radio.isChecked():
    #             return radio.objectName()
    #
    # def _open_video_button_clicked(self):
    #     """Open video button clicked signal"""
    #     #pylint: disable=E1101
    #     video_file = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'd:\\',
    #                                                        "Video files (*.mp4 *.avi)")
    #     visual_data = VisualData(video_file[0])
    #     self._control_form.set_visual_data(visual_data)
    #     #pylint: enable=E1101
    #
    # def _visual_data_updated(self, frame):
    #     """control current updated slot"""
    #     # print(current_value)
    #     self._visual_data_form.update_frame(frame)
    #
    # def _sensor_data_updated(self, central):
    #     """control current updated slot"""
    #     # print(current_value)
    #     self._sensor_data_form.update_central(central)




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
