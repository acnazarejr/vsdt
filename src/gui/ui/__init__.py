#pylint: disable=C0103
"""Gui init module"""

import os

from PyQt5 import uic

DIR = os.path.dirname(os.path.realpath(__file__))

MainWindowUi, MainWindowUiBase = uic.loadUiType(os.path.join(DIR, 'main_window.ui'))

VisualDataManagerMDIWidgetUi, VisualDataManagerMDIWidgetUiBase = uic.loadUiType(
    os.path.join(DIR, 'visual_data_manager_mdi_widget.ui'))

VisualDataViewWidgetUi, VisualDataViewWidgetUiBase = uic.loadUiType(
    os.path.join(DIR, 'visual_data_view_widget.ui'))

TimeControlWidgetUi, TimeControlWidgetUiBase = uic.loadUiType(
    os.path.join(DIR, 'time_control_widget.ui'))
