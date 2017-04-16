"""Util functions for json operations"""

import datetime

def json_handler(value):
    """JSON Handler for unknown types."""
    if isinstance(value, datetime.datetime):
        return value.isoformat()
    raise TypeError("Unknown type")
