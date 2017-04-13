#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
#pylint: disable=R0903
"""Main Window class"""

from PyQt5 import QtWidgets

from gui.ui import SensorDataManagerWindowUi

class SensorDataManagerWindow(QtWidgets.QMainWindow):
    """Main Window class"""

    def __init__(self, parent=None):
        """Init method"""
        QtWidgets.QMainWindow.__init__(self, parent)
        self.gui = SensorDataManagerWindowUi()
        self.gui.setupUi(self)

        self.gui.splitter.setStretchFactor(0, 1)
        self.gui.splitter.setStretchFactor(1, 8)

        self.gui.addButton.clicked.connect(self._add_button_clicked)

        self.gui.newSensorDataAction.triggered.connect(self._new_sensor_data_action)

    def _new_sensor_data_action(self):
        """New sensor data action"""
        self.gui.centralWidget.setEnabled(True)

    def _add_button_clicked(self):
        """Add button clicked signal"""
        topitem = QtWidgets.QTreeWidgetItem(self.gui.sensorDataTree)
        self.gui.sensorDataTree.addTopLevelItem(topitem)
        topitem.setText(0, 'teste')
