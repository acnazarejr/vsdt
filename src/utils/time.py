"""Util functions for time operations"""

import dateutil.parser

def milliseconds_to_datetime(milliseconds):
    """Converts a milliseconds time value to a datetime."""
    fraction = milliseconds%1000
    seconds = (milliseconds/1000)%60
    seconds = int(seconds)
    minutes = (milliseconds/(1000*60))%60
    minutes = int(minutes)
    hours = (milliseconds/(1000*60*60))%24
    return dateutil.parser.parse("{}:{}:{}.{}".format(hours, minutes, seconds, fraction))

def time_delta_in_milliseconds(date_a, date_b):
    """Converts a datetime difference (time delta) in milliseconds"""
    diff = (date_a - date_b)
    return diff.total_seconds() * 1000
