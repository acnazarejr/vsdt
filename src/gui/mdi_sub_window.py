"""MDISubWindow class file."""

#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtWidgets import QMdiSubWindow
from PyQt5.QtCore import Qt
from gui.base_mdi import BaseMDI
#pylint: enable=E0611
#pylint: enable=E0401

#pylint: disable=R0903
class MDISubWindow(QMdiSubWindow):
    """MDISubWindow class."""

    def __init__(self, parent=None):
        """Init method."""
        QMdiSubWindow.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose, True)
        self._widget = None

    #pylint: disable=C0103
    def setWidget(self, widget):
        """Set a widget to sub window."""
        if not isinstance(widget, BaseMDI):
            raise RuntimeError('widget must be a BaseMDI instance')
        self.setWindowTitle(widget.get_title())
        self.setWindowIcon(widget.get_icon())
        widget.title_updated.connect(self.setWindowTitle)
        super(MDISubWindow, self).setWidget(widget)
    #pylint: enable=C0103

    # def closeEvent(self, event):
    #     """close event"""
    #     print('close')
    #     event.ignore()
