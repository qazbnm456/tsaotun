"""This module contains `docker info` class"""

import json

from .command import Command


class Info(Command):
    """This class implements `docker info` command"""

    name = "info"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        self.settings[self.name] = json.dumps(
            self.client.info(), indent=4) + "\n"

    def final(self):
        return self.settings[self.name]
