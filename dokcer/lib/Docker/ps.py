"""This module contains `docker ps` class"""

import pystache
import arrow
from pytabwriter import TabWriter

from .command import Command


class Ps(Command):
    """This class implements `docker ps` command"""

    name = "ps"
    require = []

    defaultTemplate = '{{Id}}\t{{Image}}\t"{{Command}}"\t{{Created}}\t{{Status}}\t{{Ports}}\t{{Names}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def process_ports(self, ports):
        port_list = {"tcp": [], "udp": []}
        for port in ports:
            port_list[port["Type"]].append(str(port["PrivatePort"]))
        for port_type, port_value in port_list.iteritems():
            if len(port_value) == 0:
                del port_value

        return ' '.join(["{}/{}".format(','.join(port_list[port_type]), port_type) for port_type in port_list.keys()])

    def eval_command(self, args):
        tw = TabWriter()
        if args["format"] is None:
            tw.padding = [8, 8, 3, 7, 8, 11]
            fm = self.defaultTemplate
            tw.writeln(
                "CONTAINER ID\tIMAGE\tCOMMAND\tCREATED\tSTATUS\tPORTS\tNAMES")
        else:
            fm = args["format"]
        del args["format"]

        nodes = self.client.containers(**args)
        for node in nodes:
            node["Id"] = node["Id"][:12]
            node["Command"] = (node["Command"][
                               :17] + "...") if len(node["Command"]) >= 20 else node["Command"]
            node["Created"] = arrow.get(node["Created"]).humanize()
            node["Ports"] = self.process_ports(node['Ports'])
            node["Names"] = ', '.join([e[1:] for e in node["Names"]])
            tw.writeln(pystache.render(fm, node))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
