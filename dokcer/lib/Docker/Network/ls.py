"""This module contains `docker network ls` class"""

from collections import defaultdict
import pystache
from pytabwriter import TabWriter

from .command import Command


class Ls(Command):
    """This class implements `docker network ls` command"""

    name = "network ls"
    require = []

    defaultTemplate = '{{Id}}\t{{Name}}\t{{Driver}}\t{{Scope}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        tw = TabWriter()
        if args["format"] is None:
            tw.padding = [8, 14, 14]
            fm = self.defaultTemplate
            tw.writeln(
                "NETWORK ID\tNAME\tDRIVER\tSCOPE")
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

        # wait for PR: https://github.com/docker/docker-py/pull/1362
        del args["filters"]

        nodes = self.client.networks(**args)
        if nodes:
            for node in nodes:
                node["Id"] = node["Id"][:12]
                tw.writeln(pystache.render(fm, node))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
