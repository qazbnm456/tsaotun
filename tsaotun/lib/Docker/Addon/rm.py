"""This module contains `tsaotun addon rm` class"""

from .command import Command
from ....lib.Addon.loader import Loader


class Rm(Command):
    """This class implements `tsaotun addon rm` command"""

    name = "addon rm"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        loader = Loader()
        self.settings[self.name] = loader.rm(args["addon"])

    def final(self):
        return self.settings[self.name]
