"""This module contains `docker images` class"""

import pystache

from .command import Command


def pprint_images(l):
    """Pretty print"""
    return ''.join("{:25}".format(e) for e in l.split("\t")) + "\n"


class Images(Command):
    """This class implements `docker images` command"""

    name = "images"
    require = []

    defaultTemplate = '{{Repository}}\t{{Tag}}\t{{ID}}\t{{Created}} ago\t{{Size}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["format"] is None:
            fm = self.defaultTemplate
            self.settings[self.name] = pprint_images("REPOSITORY\tTAG\tIMAGE ID\tCREATED\tSIZE")
        else:
            fm = args["format"]
            self.settings[self.name] = ""
        del args["format"]

        nodes = self.client.images(**args)
        for node in nodes:
            node["ID"] = node["Id"].split(":")[1][:12]
            node["Repository"], node["Tag"] = node["RepoTags"][0].split(":")
            self.settings[self.name] += pprint_images(pystache.render(fm, node))

    def final(self):
        return self.settings[self.name]
