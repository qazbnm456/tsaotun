"""This module contains `docker images` class"""

import arrow
import humanize
import pystache

from .command import Command


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:26}".format(e) for e in l.split("\t")) + "\n"


class Images(Command):
    """This class implements `docker images` command"""

    name = "images"
    require = []

    defaultTemplate = '{{{Repository}}}\t{{{Tag}}}\t{{Id}}\t{{Created}}\t{{Size}}'
    digestsTemplate = '{{{Repository}}}\t{{{Tag}}}\t{{{Digest}}}\t{{Id}}\t{{Created}}\t{{Size}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["digests"]:
            fm = self.digestsTemplate
            self.settings[self.name] = pprint_things(
                "REPOSITORY\tTAG\tDIGEST\tIMAGE ID\tCREATED\tSIZE")
        elif args["format"] is None:
            fm = self.defaultTemplate
            self.settings[self.name] = pprint_things(
                "REPOSITORY\tTAG\tIMAGE ID\tCREATED\tSIZE")
        else:
            fm = args["format"]
            self.settings[self.name] = ""
        del args["digests"]
        del args["format"]

        args["filters"] = dict(args["filters"]) if args["filters"] else None

        nodes = self.client.images(**args)
        for node in nodes:
            node["Repository"], node["Tag"] = node["RepoTags"][0].split(":")
            node["Digest"] = node["RepoDigests"][0].split('@', 2)[1][:24]  if node["RepoDigests"] else '<' + str(node["RepoDigests"]) + '>'
            node["Id"] = node["Id"].split(":")[1][:12]
            node["Created"] = arrow.get(node["Created"]).humanize()
            node["Size"] = humanize.naturalsize(node["VirtualSize"])
            self.settings[
                self.name] += pprint_things(pystache.render(fm, node))

    def final(self):
        return self.settings[self.name]
