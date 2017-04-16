#pylint: disable=C0103
"""Gui init module"""

import os

from PyQt5 import uic

DIR = os.path.dirname(os.path.realpath(__file__))

MainWindowUi, MainWindowUiBase = uic.loadUiType(os.path.join(DIR, 'vsdt_main_window.ui'))

VisualManagerMDIUi, VisualManagerMDIUiBase = uic.loadUiType(
    os.path.join(DIR, 'visual_manager_mdi.ui'))
#
# SensorDataManagerMDIWidgetUi, SensorDataManagerMDIWidgetUiBase = uic.loadUiType(
#     os.path.join(DIR, 'sensor_data_manager_mdi_widget.ui'))
#
VisualDataViewWidgetUi, VisualDataViewWidgetUiBase = uic.loadUiType(
    os.path.join(DIR, 'visual_data_view_widget.ui'))
#
# SensorDataViewWidgetUi, SensorDataViewWidgetUiBase = uic.loadUiType(
#     os.path.join(DIR, 'sensor_data_view_widget.ui'))
#
TimeControlWidgetUi, TimeControlWidgetUiBase = uic.loadUiType(
    os.path.join(DIR, 'time_control_widget.ui'))
