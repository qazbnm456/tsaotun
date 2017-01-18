"""This module contains `tsaotun addon enable` class"""

from .command import Command
from ....lib.Addon.loader import Loader


class Enable(Command):
    """This class implements `tsaotun addon enable` command"""

    name = "addon enable"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        loader = Loader()
        self.settings[self.name] = loader.enable(args["addon"])

    def final(self):
        return self.settings[self.name]
