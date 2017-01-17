"""This module contains Placeholder class"""

from .command import Command


class Placeholder(Command):
    """This class should be overridden by addon commands"""

    name = "placeholder"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        pass

    def final(self):
        return self.settings[self.name]
