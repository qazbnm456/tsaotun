"""This module contains `tsaotun addon inspect` class"""

from .command import Command
from ....lib.Addon.loader import Loader


class Inspect(Command):
    """This class implements `tsaotun addon inspect` command"""

    name = "addon inspect"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        loader = Loader()
        self.settings[self.name] = loader.inspect(args["addon"])

    def final(self):
        return self.settings[self.name]
