#pylint: disable=E1101
"""Base form class file"""

from PyQt5 import QtWidgets, QtCore
from gui.base_mdi_widget import BaseMDIWidget

class MDISubWindow(QtWidgets.QMdiSubWindow):
    """Base Form class"""

    def __init__(self, parent=None):
        """init method"""
        QtWidgets.QMdiSubWindow.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self._widget = None

    def setWidget(self, widget):
        """set a widget to sub window"""
        if not isinstance(widget, BaseMDIWidget):
            raise AttributeError('widget must be a BaseMDIWidget instance')
        self.setWindowTitle(widget.get_title())
        self.setWindowIcon(widget.get_icon())
        widget.title_updated.connect(self.setWindowTitle)
        super(MDISubWindow, self).setWidget(widget)

    # def closeEvent(self, event):
    #     """close event"""
    #     print('close')
    #     event.ignore()
