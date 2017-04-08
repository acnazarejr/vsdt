#pylint: disable=C0103
"""Gui init module"""

import os

from PyQt5 import uic

DIR = os.path.dirname(os.path.realpath(__file__))

MainWindowUi, MainWindowUiBase = uic.loadUiType(os.path.join(DIR, 'main_window.ui'))
VisualDataFormUi, VisualDataFormUiBase = uic.loadUiType(os.path.join(DIR, 'visual_data_form.ui'))
SensorDataFormUi, SensorDataFormUiBase = uic.loadUiType(os.path.join(DIR, 'sensor_data_form.ui'))
ControlFormUi, ControlFormUiBase = uic.loadUiType(os.path.join(DIR, 'control_form.ui'))
