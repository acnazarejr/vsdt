"""TimeControl class"""

import datetime
#pylint: disable=E0611
#pylint: disable=E0401
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QIntValidator, QIcon
from gui.ui import TimeControlWidgetUi
from gui.base_widget import BaseWidget
from utils.time import time_delta_in_milliseconds
#pylint: enable=E0401
#pylint: enable=E0611

class TimeControlWidget(BaseWidget):
    """Control Widget class"""

    time_updated = pyqtSignal(datetime.datetime)
    step_updated = pyqtSignal(int)

    ###############################################################################################
    # Init
    ###############################################################################################
    def __init__(self, parent=None):
        """Init method."""
        BaseWidget.__init__(self, parent, TimeControlWidgetUi)

        self._start_time = None
        self._end_time = None
        self._interval = None
        self._current_time = None
        self._on_play = False

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_play_run)

        self.gui.playButton.clicked.connect(self._play_pause_button_clicked)
        self.gui.stopButton.clicked.connect(self._stop_button_clicked)
        self.gui.previousButton.clicked.connect(self._previous_button_clicked)
        self.gui.nextButton.clicked.connect(self._next_button_clicked)
        self.gui.gotoButton.clicked.connect(self._goto_button_clicked)
        self.gui.slider.sliderMoved.connect(self._slider_moved)

        self.setDisabled(True)
        self._refresh_info()

    ###############################################################################################
    # Public Methods
    ###############################################################################################
    def set_control_values(self, start_time=None, end_time=None, interval=None):
        """Set control values."""
        self._start_time = start_time
        self._end_time = end_time
        self._interval = interval
        self.reset()

    def set_enable(self, value):
        """Set enable or not"""
        if self._check_consistency():
            self.setEnabled(value)
            self.reset()
        else:
            self.setEnabled(False)

    def reset(self):
        """Reset controls"""
        if self._on_play:
            self.pause()
        self._current_time = self._start_time
        self.gui.slider.setMinimum(0)
        length = time_delta_in_milliseconds(self._end_time, self._start_time)
        self.gui.slider.setMaximum(length)
        validator = QIntValidator(0, int(length // self._interval))
        self.gui.currentStepField.setValidator(validator)
        self._update_current_time()

    def play(self):
        """play function"""
        self.gui.playButton.setText('Pause')
        self.gui.playButton.setIcon(QIcon(':/icons/pause.png'))
        self._on_play = True
        self.timer.start(self._interval)

    def pause(self):
        """pause function"""
        self.gui.playButton.setText('Play')
        self.gui.playButton.setIcon(QIcon(':/icons/play.png'))
        self._on_play = False
        self.timer.stop()

    ###############################################################################################
    # Private Methods
    ###############################################################################################
    def _check_consistency(self):
        """Check control values consistency"""
        if (self._start_time is None) or  (self._end_time is None):
            return False
        if self._start_time >= self._end_time:
            return False
        return True

    def _refresh_info(self):
        current = self._current_time.strftime("%H:%M:%S.%f")[:-3] \
            if self._current_time is not None else '--:--:--.---'
        end = self._end_time.strftime("%H:%M:%S.%f")[:-3] \
            if self._end_time is not None else '--:--:--.---'
        self.gui.currentLabel.setText(current)
        self.gui.lengthLabel.setText(end)
        if self._start_time is not None:
            elapsed_ms = time_delta_in_milliseconds(self._current_time, self._start_time)
            self.gui.currentStepField.setText(
                '{num:06d}'.format(num=int(elapsed_ms // self._interval)))
            length = time_delta_in_milliseconds(self._end_time, self._start_time)
            self.gui.totalStepsLabel.setText(
                'of {num:06d}'.format(num=int(length // self._interval)))

    def _play_pause_button_clicked(self):
        """Play Button Clicked signal"""
        if self._on_play:
            self.pause()
        else:
            self.play()

    def _stop_button_clicked(self):
        """Play Button Clicked signal"""
        self.reset()

    def _next_button_clicked(self):
        """Play Button Clicked signal"""
        self._current_time += datetime.timedelta(milliseconds=self._interval)
        self._update_current_time()

    def _previous_button_clicked(self):
        """Play Button Clicked signal"""
        self._current_time -= datetime.timedelta(milliseconds=self._interval)
        self._update_current_time()

    def _goto_button_clicked(self):
        """Goto Button clicked signal"""
        step = int(self.gui.currentStepField.text())
        self._current_time = self._start_time
        self._current_time += datetime.timedelta(milliseconds=(step * self._interval + 1))
        self._update_current_time()

    def _slider_moved(self, value):
        """Slider value changed signal"""
        self._current_time = self._start_time + datetime.timedelta(milliseconds=value)
        self._update_current_time()

    def _on_play_run(self):
        """Change values when control is on play"""
        self._current_time += datetime.timedelta(milliseconds=self._interval)
        if self._current_time >= self._end_time:
            self.pause()
        self._update_current_time()

    def _update_current_time(self):
        """Update current value"""
        self.gui.previousButton.setDisabled(False)
        self.gui.nextButton.setDisabled(False)
        if self._current_time <= self._start_time:
            self._current_time = self._start_time
            self.gui.previousButton.setDisabled(True)

        if self._current_time >= self._end_time:
            self._current_time = self._end_time
            self.gui.nextButton.setDisabled(True)

        elapsed_ms = time_delta_in_milliseconds(self._current_time, self._start_time)
        self.gui.slider.setValue(elapsed_ms)
        self._refresh_info()

        self.time_updated.emit(self._current_time)
        self.step_updated.emit(int(elapsed_ms // self._interval))
