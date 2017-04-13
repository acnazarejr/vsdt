#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""

import cv2
from PyQt5 import QtGui
from gui.ui import VisualDataViewWidgetUi
from gui.base_widget import BaseWidget
from gui.frame_view_widget import FrameViewWidget

class VisualDataViewWidget(BaseWidget):
    """Main Window class"""

    def __init__(self, parent=None):
        """Init method"""
        BaseWidget.__init__(self, parent, VisualDataViewWidgetUi)

        self.gui.videoViewWidget = FrameViewWidget(self.gui.viewGroupBox)
        self.gui.videoViewWidget.setObjectName("videoViewWidget")
        self.gui.viewGroupVerticalLayout.addWidget(self.gui.videoViewWidget)

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
