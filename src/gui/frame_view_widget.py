#pylint: disable=E1101
"""Frame View class file"""

from PyQt5 import QtWidgets, QtGui, QtCore

class FrameViewWidget(QtWidgets.QWidget):
    """Video View class"""

    def __init__(self, parent=None):
        super(FrameViewWidget, self).__init__(parent)
        self._frame = None

    def update_frame(self, frame):
        """frame property"""
        self._frame = frame
        self.update()

    #pylint: disable=C0103
    #pylint: disable=W0613
    def paintEvent(self, event):
        """Paint event method"""
        qp = QtGui.QPainter()
        qp.begin(self)
        if self._frame:
            self.draw_frame(qp, self._frame)
        qp.end()
    #pylint: enable=W0613
    #pylint: enable=C0103

    def draw_frame(self, painter, frame):
        """Draw frame into widget"""

        window_width = self.frameSize().width()
        window_height = self.frameSize().height()
        size = frame.size()

        scale_w = float(window_width) / float(size.width())
        scale_h = float(window_height) / float(size.height())
        scale = min([scale_w, scale_h])
        if scale == 0:
            scale = 1

        frame = frame.scaled(size * scale)

        image_rect = QtCore.QRect(frame.rect())
        widget_rect = QtCore.QRect(0, 0, window_width, window_height)
        image_rect.moveCenter(widget_rect.center())
        painter.drawImage(image_rect.topLeft(), frame)
