"""FrameViewWidget class file."""

#pylint: disable=E0611
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import QRect
#pylint: enable=E0611

class FrameViewWidget(QWidget):
    """FrameViewWidget class."""

    def __init__(self, parent=None):
        """Init method"""
        super(FrameViewWidget, self).__init__(parent)
        self._frame = None

    def update_frame(self, frame):
        """Update and display frame"""
        self._frame = frame
        self.update()

    def paintEvent(self, event):
        """Paint event method."""
        #pylint: disable=C0103
        #pylint: disable=W0613
        qp = QPainter()
        qp.begin(self)
        if self._frame:
            self.draw_frame(qp, self._frame)
        qp.end()
        #pylint: enable=W0613
        #pylint: enable=C0103

    def draw_frame(self, painter, frame):
        """Draw frame into widget."""
        window_width = self.frameSize().width()
        window_height = self.frameSize().height()
        size = frame.size()
        scale_w = float(window_width) / float(size.width())
        scale_h = float(window_height) / float(size.height())
        scale = min([scale_w, scale_h])
        if scale == 0:
            scale = 1
        frame = frame.scaled(size * scale)
        image_rect = QRect(frame.rect())
        widget_rect = QRect(0, 0, window_width, window_height)
        image_rect.moveCenter(widget_rect.center())
        painter.drawImage(image_rect.topLeft(), frame)
