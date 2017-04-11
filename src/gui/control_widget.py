#pylint: disable=C0103
#pylint: disable=E1101
#pylint: disable=E0611
#pylint: disable=E0401
"""Main Window class"""

from enum import Enum
from PyQt5 import QtCore, QtGui

from gui.ui import ControlWidgetUi
from gui.base_form import BaseForm

class ControlMode(Enum):
    """Control Mode enum"""
    FRAME = 1
    TIME = 2
    FRAME_TIME = 3

class ControlWidget(BaseForm):
    """Control Widget class"""

    time_updated = QtCore.pyqtSignal(object)
    step_updated = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        """Init method"""
        BaseForm.__init__(self, parent, ControlWidgetUi)

        self._start_time = None
        self._end_time = None
        self._interval = None

        self._current_time = None
        self._on_play = False

        self._operation_mode = ControlMode.FRAME_TIME

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._on_play_run)
        #self.timer.start(1)

        self.gui.playButton.clicked.connect(self._play_pause_button_clicked)
        self.gui.stopButton.clicked.connect(self._stop_button_clicked)
        self.gui.previousButton.clicked.connect(self._previous_button_clicked)
        self.gui.nextButton.clicked.connect(self._next_button_clicked)

        self.gui.slider.valueChanged.connect(self._slider_value_changed)
        self.gui.slider.sliderMoved.connect(self._slider_moved)

        self.setDisabled(True)
        self._reflesh_time_label()


    def set_control_values(self, start_time=None, end_time=None, interval=None):
        """Set control values"""
        self._start_time = start_time
        self._end_time = end_time
        self._interval = interval
        self.reset()

    def set_enable(self, value):
        """Set enable or not"""
        if self._check_consistency:
            self.setEnabled(value)
        else:
            self.setEnabled(False)
        self.reset()

    def reset(self):
        """Reset controls"""
        self._current_time = self._start_time
        self.gui.slider.setMinimum(self._start_time)
        self.gui.slider.setMaximum(self._end_time)
        self.timer.stop()
        self._on_play = False
        self.update_current_time()

    def _check_consistency(self):
        """Check control values consistency"""
        if self._start_time <= self._end_time:
            return False
        return True


    # def set_visual_data(self, visual_data):
    #     """Update control values"""
    #     self._visual_data = visual_data
    #     self._start_time = self._visual_data.start_time
    #     self._end_time = self._visual_data.end_time
    #     self._interval = self._visual_data.interval
    #     if self._check_consistency():
    #         self._current_time = self._start_time
    #         self.gui.slider.setMinimum(self._start_time)
    #         self.gui.slider.setMaximum(self._end_time)
    #         self.update_current_time()

    def _reflesh_time_label(self):
        current = str(self._current_time) if self._current_time is not None else '-----'
        end = str(self._end_time) if self._end_time is not None else '-----'
        self.gui.timeLabel.setText("{} / {}".format(current, end))

    def _play_pause_button_clicked(self):
        """Play Button Clicked signal"""
        if self._on_play:
            self.pause()
        else:
            self.play()

    def _stop_button_clicked(self):
        """Play Button Clicked signal"""
        if self._on_play:
            self.pause()
        self.reset()
        self.update_current_time()

    def _next_button_clicked(self):
        """Play Button Clicked signal"""
        self._current_time += self._interval
        self.update_current_time()

    def _previous_button_clicked(self):
        """Play Button Clicked signal"""
        self._current_time -= self._interval
        self.update_current_time()

    def _slider_value_changed(self, value):
        """Slider value changed signal"""
        # self._current_time = value
        # print(value)
        pass

    def _slider_moved(self, value):
        """Slider value changed signal"""
        self._current_time = value
        self.update_current_time()

    def play(self):
        """play function"""
        self.gui.playButton.setText('Pause')
        self.gui.playButton.setIcon(QtGui.QIcon(':/icons/pause.png'))
        self._on_play = True
        self.timer.start(self._interval)

    def pause(self):
        """pause function"""
        self.gui.playButton.setText('Play')
        self.gui.playButton.setIcon(QtGui.QIcon(':/icons/play.png'))
        self._on_play = False
        self.timer.stop()

    def _on_play_run(self):
        """Change values when control is on play"""
        self._current_time += self._interval
        if self._current_time >= self._end_time:
            self.pause()
        self.update_current_time()

    def update_current_time(self):
        """Update current value"""
        self.gui.previousButton.setDisabled(False)
        self.gui.nextButton.setDisabled(False)
        if self._current_time <= self._start_time:
            self._current_time = self._start_time
            self.gui.previousButton.setDisabled(True)

        if self._current_time >= self._end_time:
            self._current_time = self._end_time
            self.gui.nextButton.setDisabled(True)

        self.gui.slider.setValue(self._current_time)
        self._reflesh_time_label()

        self.time_updated.emit(self._current_time)
        self.step_updated.emit(self._current_time // self._interval)
