"""This module contains `docker volume ls` class"""

from collections import defaultdict
import pystache

from .command import Command


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:25}".format(e) for e in l.split("\t")) + "\n"


class Ls(Command):
    """This class implements `docker volume ls` command"""

    name = "volume ls"
    require = []

    defaultTemplate = '{{Driver}}\t{{Name}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["format"] is None:
            fm = self.defaultTemplate
            self.settings[self.name] = pprint_things(
                "DRIVER\tVOLUME NAME")
        else:
            fm = args["format"]
            self.settings[self.name] = ""
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
                self.settings[self.name] += pprint_things(pystache.render(fm, node))

    def final(self):
        return self.settings[self.name]
