"""Util functions for files manipulation"""

import os

def is_path_creatable(path_name):
    """Check if a path is creatable or not."""
    return os.path.exists(path_name) or os.access(os.path.dirname(path_name), os.W_OK)
