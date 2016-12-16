"""This module contains `docker ps` class"""

import pystache
import arrow

from .command import Command


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:25}".format(e) for e in l.split("\t")) + "\n"


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
        for port_type in port_list.keys():
            if len(port_list[port_type]) == 0:
                del port_list[port_type]

        return ' '.join(["{}/{}".format(','.join(port_list[port_type]), port_type) for port_type in port_list.keys()])

    def eval_command(self, args):
        if args["format"] is None:
            fm = self.defaultTemplate
            self.settings[self.name] = pprint_things(
                "CONTAINER ID\tIMAGE\tCOMMAND\tCREATED\tSTATUS\tPORTS\tNAMES")
        else:
            fm = args["format"]
            self.settings[self.name] = ""
        del args["format"]

        nodes = self.client.containers(**args)
        for node in nodes:
            node["Id"] = node["Id"][:12]
            node["Created"] = arrow.get(node["Created"]).humanize()
            node["Ports"] = self.process_ports(node['Ports'])
            node["Names"] = ', '.join([e[1:] for e in node["Names"]])
            self.settings[self.name] += pprint_things(pystache.render(fm, node))

    def final(self):
        return self.settings[self.name]
