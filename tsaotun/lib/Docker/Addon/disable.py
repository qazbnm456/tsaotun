"""This module contains `tsaotun addon disable` class"""

from .command import Command
from ....lib.Addon.loader import Loader


class Disable(Command):
    """This class implements `tsaotun addon disable` command"""

    name = "addon disable"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        loader = Loader()
        self.settings[self.name] = loader.disable(args["addon"])

    def final(self):
        return self.settings[self.name]
