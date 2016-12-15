"""This module contains `docker history` class"""

import arrow
import humanize
import pystache

from .command import Command

def pprint_images(l):
    """Pretty print"""
    return ''.join("{:26}".format(e) for e in l.split("\t")) + "\n"


class History(Command):
    """This class implements `docker history` command"""

    name = "history"
    require = []

    defaultTemplate = '{{{Id}}}\t{{Created}}\t{{{CreatedBy}}}\t{{Size}}\t{{Comment}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        fm = self.defaultTemplate
        self.settings[self.name] = pprint_images(
            "IMAGE\tCREATED\tCREATED BY\tSIZE\tCOMMENT")
        nodes = self.client.history(**args)
        for node in nodes:
            try:
                node["Id"] = node["Id"].split(":")[1][:12]
            except IndexError:
                pass
            node["Created"] = arrow.get(node["Created"]).humanize()
            node["CreatedBy"] = node["CreatedBy"][:18] + "..."
            node["Size"] = humanize.naturalsize(node["Size"])
            self.settings[
                self.name] += pprint_images(pystache.render(fm, node))

    def final(self):
        return self.settings[self.name]