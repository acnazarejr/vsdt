"""Util functions for GUI operations"""

import os.path
#pylint: disable=E0611
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtCore import QSettings
#pylint: enable=E0611

def get_settings():
    """Get global qsettings."""
    return QSettings('vsdt', 'vsdt')

def get_open_file(parent, title, file_filter, suggestion=None):
    """Open a file and stores the last dir open."""
    settings = get_settings()
    last_dir = settings.value('last_dir', type=str)
    if suggestion is None:
        suggestion = last_dir
    opened_file = QFileDialog.getOpenFileName(parent, title, last_dir, file_filter)[0]
    opened_file = opened_file if opened_file != '' else None
    if opened_file is not None:
        open_dir = os.path.dirname(opened_file)
        settings.setValue('last_dir', open_dir)
    return opened_file

def get_open_files(parent, title, file_filter, suggestion=None):
    """Open a set of files and stores the last dir open."""
    settings = get_settings()
    last_dir = settings.value('last_dir', type=str)
    if suggestion is None:
        suggestion = last_dir
    files = QFileDialog.getOpenFileNames(parent, title, last_dir, file_filter)[0]
    if files:
        open_dir = os.path.dirname(files[0])
        settings.setValue('last_dir', open_dir)
    return files

def get_save_file(parent, title, file_filter, suggestion=None):
    """Get a path to save a file."""
    settings = get_settings()
    last_dir = settings.value('last_dir', type=str)
    if suggestion is None:
        suggestion = last_dir
    saved_file = QFileDialog.getSaveFileName(parent, title, suggestion, file_filter)[0]
    saved_file = saved_file if saved_file != '' else None
    return saved_file

def save_message_box(parent=None):
    """Save message box."""
    msg_box = QMessageBox(parent)
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setText("The data has been modified.")
    msg_box.setInformativeText("Do you want to save your changes?")
    msg_box.setStandardButtons(QMessageBox.Save |
                               QMessageBox.Discard |
                               QMessageBox.Cancel)
    msg_box.setDefaultButton(QMessageBox.Save)
    return msg_box.exec_()
