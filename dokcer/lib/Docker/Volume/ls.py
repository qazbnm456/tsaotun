"""This module contains `docker volume ls` class"""

from collections import defaultdict
import pystache
from pytabwriter import TabWriter

from .command import Command


class Ls(Command):
    """This class implements `docker volume ls` command"""

    name = "volume ls"
    require = []

    defaultTemplate = '{{Driver}}\t{{Name}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        tw = TabWriter()
        if args["format"] is None:
            tw.padding = [14]
            fm = self.defaultTemplate
            tw.writeln(
                "DRIVER\tVOLUME NAME")
        else:
            fm = args["format"]
        del args["format"]

        if args["filters"]:
            filters = args["filters"]
            args["filters"] = []
            d = defaultdict(list)
            for k, v in filters:
                d[k].append(v)
            args["filters"] = dict(d)

        nodes = self.client.volumes(**args)["Volumes"]
        if nodes:
            for node in nodes:
                tw.writeln(pystache.render(fm, node))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
