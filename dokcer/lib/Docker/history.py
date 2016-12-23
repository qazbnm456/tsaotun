"""This module contains `docker history` class"""

import arrow
import humanize
import pystache
from pytabwriter import TabWriter

from .command import Command


class History(Command):
    """This class implements `docker history` command"""

    name = "history"
    require = []

    defaultTemplate = '{{{Id}}}@{{Created}}@{{{CreatedBy}}}@{{Size}}@{{Comment}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        tw = TabWriter(tabchar='@')
        tw.padding = [8, 9, 3, 8]
        fm = self.defaultTemplate
        tw.writeln(
            "IMAGE@CREATED@CREATED BY@SIZE@COMMENT")
        nodes = self.client.history(**args)
        if nodes:
            for node in nodes:
                node["Id"] = node["Id"].split(":")[1][:12] if ":" in node[
                    "Id"] else node["Id"]
                node["Created"] = arrow.get(node["Created"]).humanize()
                node["CreatedBy"] = (node["CreatedBy"][
                    :42] + "...") if len(node["CreatedBy"]) >= 45 else node["CreatedBy"]
                node["Size"] = humanize.naturalsize(node["Size"])
                tw.writeln(pystache.render(fm, node))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
