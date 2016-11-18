"""This module contains `docker ps` class"""

import pystache

from .command import Command


def pprint_ps(l):
    """Pretty print"""
    return ''.join("{:25}".format(e) for e in l.split("\t")) + "\n"


class Ps(Command):
    """This class implements `docker ps` command"""

    name = "ps"
    require = []

    defaultTemplate = '{{ID}}\t{{Image}}\t"{{Command}}"\t{{Created}} ago\t{{Status}}\t{{Ports}}\t{{Names}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["format"] is None:
            fm = self.defaultTemplate
            self.settings[self.name] = pprint_ps("CONTAINER ID\tIMAGE\tCOMMAND\tCREATED\tSTATUS\tPORTS\tNAMES")
        else:
            fm = args["format"]
            self.settings[self.name] = ""
        del args["format"]

        nodes = self.client.containers(**args)
        for node in nodes:
            node["ID"] = node["Id"][:12]
            node["Names"] = ', '.join([e[1:] for e in node["Names"]])
            self.settings[self.name] += pprint_ps(pystache.render(fm, node))

    def final(self):
        return self.settings[self.name]
