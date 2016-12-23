"""This module contains `docker images` class"""

import arrow
import humanize
import pystache
from pytabwriter import TabWriter

from .command import Command


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
        tw = TabWriter()
        if args["digests"]:
            tw.padding = [3, 10, 3, 8, 8]
            fm = self.digestsTemplate
            tw.writeln(
                "REPOSITORY\tTAG\tDIGEST\tIMAGE ID\tCREATED\tSIZE")
        elif args["format"] is None:
            tw.padding = [3, 10, 8, 8]
            fm = self.defaultTemplate
            tw.writeln(
                "REPOSITORY\tTAG\tIMAGE ID\tCREATED\tSIZE")
        else:
            fm = args["format"]
            self.settings[self.name] = ""
        del args["digests"]
        del args["format"]

        args["filters"] = dict(args["filters"]) if args["filters"] else None

        nodes = self.client.images(**args)
        for node in nodes:
            try:
                node["Repository"], node["Tag"] = node[
                    "RepoTags"][0].split(":")
            except TypeError:
                node["Repository"] = node["RepoDigests"][0].split('@', 2)[0]
                node["Tag"] = "<none>"
            node["Digest"] = node["RepoDigests"][0].split('@', 2)[1] if node[
                "RepoDigests"] else '<' + str(node["RepoDigests"]) + '>'
            node["Id"] = node["Id"].split(":")[1][:12]
            node["Created"] = arrow.get(node["Created"]).humanize()
            node["Size"] = humanize.naturalsize(node["VirtualSize"])
            tw.writeln(pystache.render(fm, node))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
