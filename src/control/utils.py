#pylint: disable=E1101
#pylint: disable=E0401
"""Util functions"""

import datetime
import dateutil.parser

def milliseconds_to_timestamp(milliseconds):
    """method for milliseconds to timestamp converting"""
    fraction = milliseconds%1000
    seconds = (milliseconds/1000)%60
    seconds = int(seconds)
    minutes = (milliseconds/(1000*60))%60
    minutes = int(minutes)
    hours = (milliseconds/(1000*60*60))%24

    return dateutil.parser.parse("{}:{}:{}.{}".format(hours, minutes, seconds, fraction))

def time_delta_in_milliseconds(date_a, date_b):
    """get difference of two timestamps in milliseconds"""
    diff = (date_a - date_b)
    return diff.total_seconds() * 1000

def datetime_handler(timestamp):
    """handle for timestamps"""
    if isinstance(timestamp, datetime.datetime):
        return timestamp.isoformat()
    raise TypeError("Unknown type")
