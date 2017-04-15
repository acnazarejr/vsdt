#pylint: disable=E1101
#pylint: disable=E0401
"""Util functions for gui"""

import os.path
from PyQt5 import QtWidgets, QtCore

def get_settings():
    """Get global qsettings"""
    return QtCore.QSettings('vsdt', 'vsdt')

def get_open_file(parent, title, file_filter, suggestion=None):
    """Open a file and stores the last dir open"""
    settings = get_settings()
    last_dir = settings.value('last_dir', type=str)
    if suggestion is None:
        suggestion = last_dir
    opened_file = QtWidgets.QFileDialog.getOpenFileName(parent, title, last_dir, file_filter)[0]
    opened_file = opened_file if opened_file != '' else None
    if opened_file is not None:
        open_dir = os.path.dirname(opened_file)
        settings.setValue('last_dir', open_dir)
    return opened_file

def get_open_files(parent, title, file_filter, suggestion=None):
    """Open a file and stores the last dir open"""
    settings = get_settings()
    last_dir = settings.value('last_dir', type=str)
    if suggestion is None:
        suggestion = last_dir
    files = QtWidgets.QFileDialog.getOpenFileNames(parent, title, last_dir, file_filter)[0]
    if files:
        open_dir = os.path.dirname(files[0])
        settings.setValue('last_dir', open_dir)
    return files

def get_save_file(parent, title, file_filter, suggestion=None):
    """Open a file and stores the last dir open"""
    settings = get_settings()
    last_dir = settings.value('last_dir', type=str)
    if suggestion is None:
        suggestion = last_dir
    saved_file = QtWidgets.QFileDialog.getSaveFileName(parent, title, suggestion, file_filter)[0]
    saved_file = saved_file if saved_file != '' else None
    return saved_file

def save_message_box(parent=None):
    """message box for save question"""
    msg_box = QtWidgets.QMessageBox(parent)
    msg_box.setIcon(QtWidgets.QMessageBox.Question)
    msg_box.setText("The data has been modified.")
    msg_box.setInformativeText("Do you want to save your changes?")
    msg_box.setStandardButtons(QtWidgets.QMessageBox.Save |
                               QtWidgets.QMessageBox.Discard |
                               QtWidgets.QMessageBox.Cancel)
    msg_box.setDefaultButton(QtWidgets.QMessageBox.Save)
    return msg_box.exec_()
