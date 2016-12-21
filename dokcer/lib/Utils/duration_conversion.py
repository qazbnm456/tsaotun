# -*- coding: UTF-8 -*-
"""
This module provides converting between datetime.timedelta and Go's Duration strings.
Taken from https://github.com/icholy/Duration.py/, and made by icholy.
"""

import re
import datetime

_nanosecond_size = 1
_microsecond_size = 1000 * _nanosecond_size
_millisecond_size = 1000 * _microsecond_size
_second_size = 1000 * _millisecond_size
_minute_size = 60 * _second_size
_hour_size = 60 * _minute_size

units = {
    "ns": _nanosecond_size,
    "us": _microsecond_size,
    "µs": _microsecond_size,
    "μs": _microsecond_size,
    "ms": _millisecond_size,
    "s": _second_size,
    "m": _minute_size,
    "h": _hour_size
}


def from_str(duration):
    """Parse a duration string to a datetime.timedelta"""

    if duration in ("0", "+0", "-0"):
        return datetime.timedelta()

    pattern = re.compile('([\-\+\d\.]+)([a-zµμ]+)')
    total = 0
    sign = -1 if duration[0] == '-' else 1
    matches = pattern.findall(duration)

    if not len(matches):
        raise Exception("Invalid duration {}".format(duration))

    for (value, unit) in matches:
        if unit not in units:
            raise Exception(
                "Unknown unit {} in duration {}".format(unit, duration))
        try:
            total += float(value) * units[unit]
        except:
            raise Exception(
                "Invalid value {} in duration {}".format(value, duration))

    microseconds = total / _microsecond_size
    return datetime.timedelta(microseconds=sign * microseconds)


def to_str(delta):
    """Format a datetime.timedelta to a duration string"""

    total_seconds = delta.total_seconds()
    sign = "-" if total_seconds < 0 else ""
    nanoseconds = abs(total_seconds * _second_size)

    if total_seconds < 1:
        result_str = _to_str_small(nanoseconds)
    else:
        result_str = _to_str_large(nanoseconds)

    return "{}{}".format(sign, result_str)


def _to_str_small(nanoseconds):

    result_str = ""

    if not nanoseconds:
        return "0"

    milliseconds = int(nanoseconds / _millisecond_size)
    if milliseconds:
        nanoseconds -= _millisecond_size * milliseconds
        result_str += "{}ms".format(milliseconds)

    microseconds = int(nanoseconds / _microsecond_size)
    if microseconds:
        nanoseconds -= _microsecond_size * microseconds
        result_str += "{}us".format(microseconds)

    if nanoseconds:
        result_str += "{}ns".format(nanoseconds)

    return result_str


def _to_str_large(nanoseconds):

    result_str = ""

    hours = int(nanoseconds / _hour_size)
    if hours:
        nanoseconds -= _hour_size * hours
        result_str += "{}h".format(hours)

    minutes = int(nanoseconds / _minute_size)
    if minutes:
        nanoseconds -= _minute_size * minutes
        result_str += "{}m".format(minutes)

    seconds = float(nanoseconds) / float(_second_size)
    if seconds:
        nanoseconds -= _second_size * seconds
        result_str += "{}s".format(seconds)

    return result_str
