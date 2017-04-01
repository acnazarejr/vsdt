#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""

from PyQt5 import QtCore

from gui.ui import ControlFormUi
from gui.base_form import BaseForm

#from app.modules.sensors.webcam import WebCam

class ControlForm(BaseForm):
    """Main Window class"""

    refresh = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Init method"""
        BaseForm.__init__(self, parent, ControlFormUi)

        self._start = None
        self._end = None
        self._interval = None
        self._current = None
        self._on_play = False

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._on_play_run)
        #self.timer.start(1)

        self.gui.playButton.clicked.connect(self._play_button_clicked)
        self.gui.stopButton.clicked.connect(self._stop_button_clicked)
        self.gui.slider.valueChanged.connect(self._slider_value_changed)

    def update_values(self, start, end, interval):
        """Update control values"""
        self._start = start
        self._end = end
        self._interval = interval
        self._current = self._start
        self.gui.slider.setMinimum(self._start)
        self.gui.slider.setMaximum(self._end)
        self.update_current(self._current)

    def _play_button_clicked(self):
        """Play Button Clicked signal"""
        if self._on_play:
            self.pause()
        else:
            self.play()

    def _stop_button_clicked(self):
        """Play Button Clicked signal"""
        if self._on_play:
            self.pause()
        self._on_play = False
        self._current = self._start
        self.gui.slider.setValue(self._current)

    def _slider_value_changed(self, value):
        """Slider value changed signal"""
        self._current = value
        self.update_current(self._current)

    def play(self):
        """play function"""
        self.gui.playButton.setText('Pause')
        self._on_play = True
        self.timer.start(self._interval)

    def pause(self):
        """pause function"""
        self.gui.playButton.setText('Play')
        self._on_play = False
        self.timer.stop()

    def _on_play_run(self):
        """Change values when control is on play"""
        self._current += self._interval
        if self._current >= self._end:
            self.timer.stop()
        else:
            self.gui.slider.setValue(self._current)

    def update_current(self, current):
        """Update current value"""
        print('current', current)
