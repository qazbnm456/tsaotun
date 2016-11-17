import os
import sys
from abc import ABCMeta, abstractmethod
from six import with_metaclass

class Command(with_metaclass(ABCMeta, object)):
    """
    This class represents a command, it must be extended
    for any class which implements a type of command
    """

    name = "command"
    client = None

    def __init__(self):
        self.settings = {}

        # List of commands that must be launched during the current command
        # Must be left empty in the code
        self.deps = []

    @abstractmethod
    def evalCommand(self, args):
        pass

    def final(self):
        return self.settings

    def loadRequire(self, args, obj=[]):
        self.deps = obj
        for x in self.deps:
            x.evalCommand(args)

    def Command(self, args, client):
        self.client = client
        self.evalCommand(args)
        return self.final()
