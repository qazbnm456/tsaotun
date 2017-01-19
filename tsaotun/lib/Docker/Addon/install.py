"""This module contains `tsaotun addon install` class"""

from .command import Command
from ....lib.Addon.loader import Loader


class Install(Command):
    """This class implements `tsaotun addon install` command"""

    name = "addon install"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        loader = Loader()
        self.settings[self.name] = loader.install(args["addon"], args["alias"])

    def final(self):
        return self.settings[self.name]
