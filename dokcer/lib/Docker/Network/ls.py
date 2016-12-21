"""This module contains `docker network ls` class"""

from collections import defaultdict
import pystache

from .command import Command


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:25}".format(e) for e in l.split("\t")) + "\n"


class Ls(Command):
    """This class implements `docker network ls` command"""

    name = "network ls"
    require = []

    defaultTemplate = '{{Id}}\t{{Name}}\t{{Driver}}\t{{Scope}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["format"] is None:
            fm = self.defaultTemplate
            self.settings[self.name] = pprint_things(
                "NETWORK ID\tNAME\tDRIVER\tSCOPE")
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

        # wait for PR: https://github.com/docker/docker-py/pull/1362
        del args["filters"]

        nodes = self.client.networks(**args)
        if nodes:
            for node in nodes:
                node["Id"] = node["Id"][:12]
                self.settings[self.name] += pprint_things(pystache.render(fm, node))

    def final(self):
        return self.settings[self.name]
