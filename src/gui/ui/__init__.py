#pylint: disable=C0103
"""Gui init module"""

import os

from PyQt5 import uic

DIRNAME = os.path.dirname(os.path.realpath(__file__))

MainWindowUi, MainWindowUiBase = uic.loadUiType(os.path.join(DIRNAME, 'main_window.ui'))
VisualDataFormUi, VisualDataFormUiBase = uic.loadUiType(
    os.path.join(DIRNAME, 'visual_data_form.ui'))
ControlFormUi, ControlFormUiBase = uic.loadUiType(os.path.join(DIRNAME, 'control_form.ui'))
