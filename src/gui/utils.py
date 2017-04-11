#pylint: disable=E1101
#pylint: disable=E0401
"""Util functions for gui"""

import os.path
from PyQt5 import QtWidgets
from models import VisualData

def open_visual_data(parent):
    """Dialog for open visual data"""
    control_var = False
    visual_data = None
    while not control_var:
        dialog_ret = QtWidgets.QFileDialog.getOpenFileName(parent, 'Open file', 'd:\\',
                                                           "Video files (*.mp4 *.avi)")
        video_file = dialog_ret[0]
        visual_data = VisualData(video_file)
        if (not os.path.isfile(video_file)) or (not visual_data.is_opened()):
            msg = "Invalid video file. Do you want to retry?"
            reply = QtWidgets.QMessageBox.question(parent, 'Message', msg,
                                                   QtWidgets.QMessageBox.Yes,
                                                   QtWidgets.QMessageBox.No)
            if reply != QtWidgets.QMessageBox.Yes:
                control_var = True
        else:
            control_var = True
    return visual_data
