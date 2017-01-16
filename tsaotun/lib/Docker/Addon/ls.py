"""This module contains `tsaotun addon ls` class"""

import pystache
from pytabwriter import TabWriter

from .command import Command
from ....lib.Addon.loader import Loader


class Ls(Command):
    """This class implements `tsaotun addon ls` command"""

    name = "addon ls"
    require = []

    defaultTemplate = '{{Addon}}\t{{Enabled}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        loader = Loader()
        tw = TabWriter()
        tw.padding = [14]
        fm = self.defaultTemplate
        tw.writeln(
            "ADDON NAME\tENABLED")

        nodes = loader.addons()
        if nodes:
            for node in nodes:
                tw.writeln(pystache.render(fm, node))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
