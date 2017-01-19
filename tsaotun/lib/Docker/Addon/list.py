"""This module contains `tsaotun addon list` class"""

import pystache
from py_tabwriter import TabWriter

from .command import Command
from ....lib.Addon.loader import Loader


class List(Command):
    """This class implements `tsaotun addon list` command"""

    name = "addon list"
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
