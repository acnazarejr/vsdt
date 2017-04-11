#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""

from PyQt5 import QtWidgets

from gui.ui import FrameTemporalSyncWindowUi
from gui.control_widget import ControlWidget
from gui.visual_data_form import VisualDataForm
from gui.utils import open_visual_data


class FrameTemporalSyncWindow(QtWidgets.QMainWindow):
    """Main Window class"""


    def __init__(self, parent=None):
        """Init method"""
        QtWidgets.QMainWindow.__init__(self, parent)
        self.gui = FrameTemporalSyncWindowUi()
        self.gui.setupUi(self)

        self._visual_data = None

        self._visual_data_form = VisualDataForm()
        self._control_widget = ControlWidget()
        self.gui.framesViewGroupVerticalLayout.addWidget(self._visual_data_form)
        self.gui.framesViewGroupVerticalLayout.addWidget(self._control_widget)

        self.gui.openVideoButton.clicked.connect(self._open_video_button_clicked)
        self._control_widget.time_updated.connect(self._visual_data_updated)

    def _open_video_button_clicked(self):
        """Open video button clicked signal"""
        self._visual_data = open_visual_data(self)
        self._control_widget.set_control_values(start_time=self._visual_data.start_time,
                                                end_time=self._visual_data.end_time,
                                                interval=self._visual_data.interval)
        self._control_widget.set_enable(True)

    def _visual_data_updated(self, time):
        """control current updated slot"""
        frame = self._visual_data.get_frame(time)
        self._visual_data_form.update_frame(frame)
