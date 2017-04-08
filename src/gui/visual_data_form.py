#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""

import cv2
from PyQt5 import QtCore, QtGui

from gui.ui import VisualDataFormUi
from gui.base_form import BaseForm
from gui.frame_view_widget import FrameViewWidget



class VisualDataForm(BaseForm):
    """Main Window class"""

    # setupButtonClicked = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Init method"""
        BaseForm.__init__(self, parent, VisualDataFormUi)

        self.gui.videoViewWidget = FrameViewWidget(self.gui.viewGroupBox)
        self.gui.videoViewWidget.setObjectName("videoViewWidget")
        self.gui.viewGroupVerticalLayout.addWidget(self.gui.videoViewWidget)

        # self.timer = QtCore.QTimer(self)
        # self.timer.timeout.connect(self.update_frame)
        # self.timer.start(1)

        # self.gui.setupButton.clicked.connect(self.setup_button_clicked)

    # def setup_button_clicked(self):
    #     """Setup Button Clicked signal"""
    #     self.setupButtonClicked.emit()

    def update_frame(self, frame):
        """temp method"""

        if frame is None:
            print('None')
            return
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, bpc = frame.shape
        bpl = bpc * width
        image = QtGui.QImage(frame.data, width, height, bpl, QtGui.QImage.Format_RGB888)
        self.gui.videoViewWidget.update_frame(image)

    def closeEvent(self, _):
        """Close event method"""
        self.video_control.pause()