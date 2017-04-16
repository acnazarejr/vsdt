"""VisualData class file."""

import cv2
#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QVBoxLayout
from gui.ui import VisualDataViewWidgetUi
from gui.base_widget import BaseWidget
from gui.frame_view_widget import FrameViewWidget
#pylint: enable=E0401
#pylint: enable=E0611

#pylint: disable=R0903
class VisualDataViewWidget(BaseWidget):
    """VisualData class."""

    def __init__(self, parent=None):
        """Init method."""
        BaseWidget.__init__(self, parent, VisualDataViewWidgetUi)

        self._frame_view_widget = FrameViewWidget(self)
        layout = QVBoxLayout(self.gui.viewGroup)
        layout.addWidget(self._frame_view_widget)
        self.gui.viewGroup.setLayout(layout)

    def update_frame(self, frame):
        """Update frame method."""
        if frame is None:
            return
        #pylint: disable=E1101
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #pylint: enable=E1101
        height, width, bpc = frame.shape
        bpl = bpc * width
        image = QImage(frame.data, width, height, bpl, QImage.Format_RGB888)
        self._frame_view_widget.update_frame(image)
