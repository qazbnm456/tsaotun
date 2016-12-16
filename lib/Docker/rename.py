"""This module contains `docker rename` class"""

import json

from .command import Command


class Rename(Command):
    """This class implements `docker rename` command"""

    name = "rename"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        self.client.rename(**args)
        self.settings[self.name] = "\r"

    def final(self):
        return self.settings[self.name]
