"""This module contains Logger class"""

import sys


class Logger(object):
    """Logger class"""

    # Color codes
    STD = "\033[0;0m"
    BLUE = "\033[1;34m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[1;33m"

    def __init__(self):
        pass

    @classmethod
    def log(cls, fmt_string, *args):
        if len(args) == 0:
            print fmt_string,
        else:
            print fmt_string.format(*args),

    @classmethod
    def logInfo(cls, fmt_string, *args):
        sys.stdout.write(cls.BLUE)
        cls.log(fmt_string, *args)
        sys.stdout.write(cls.STD)

    @classmethod
    def logWarning(cls, fmt_string, *args):
        sys.stdout.write(cls.YELLOW)
        cls.log(fmt_string, *args)
        sys.stdout.write(cls.STD)

    @classmethod
    def logError(cls, fmt_string, *args):
        sys.stdout.write(cls.RED)
        cls.log(fmt_string, *args)
        sys.stdout.write(cls.STD)

    @classmethod
    def logSuccess(cls, fmt_string, *args):
        sys.stdout.write(cls.GREEN)
        cls.log(fmt_string, *args)
        sys.stdout.write(cls.STD)

    @classmethod
    def logProgressInfo(cls, fmt_string, *args):
        sys.stdout.write(cls.BLUE)
        if len(args) == 0:
            sys.stdout.write(fmt_string)
        else:
            sys.stdout.write(fmt_string.format(*args))
        sys.stdout.write(cls.STD)
