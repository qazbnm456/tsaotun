"""This module contains `docker stats` class"""

import colorama
import humanize
import pystache

from .command import Command


colorama.init()
info = {
    "title": "",
    "layers": {},
    "final": []
}


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:20}".format(e) for e in l.split("\t")) + "\n"


def put_cursor(x, y):
    print "\x1b[{};{}H".format(y + 1, x + 1)

def clear():
    print "\x1b[2J"


class Stats(Command):
    """This class implements `docker stats` command"""

    name = "stats"
    require = []

    defaultTemplate = '{{Id}}\t{{Cpu}}%\t{{MemUsage}} / {{Limit}}\t{{Mem}}%\t{{NetInput}} / {{NetOutput}}\t0 B / 0 B\t{{Pids}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            stats = []
            containers = args["containers"]
            del args["containers"]
            args["decode"] = True
            for container in containers:
                args["container"] = container
                stats.append(self.client.stats(**args))
                """
                for line in self.client.stats(**args):
                    for iterElement in list(json_iterparse.json_iterparse(line)):
                        # self.output(iterElement, args)
                        print iterElement
                """
            clear()
            put_cursor(0, 0)
            print pprint_things(
                "CONTAINER\tCPU %\tMEM USAGE / LIMIT\tMEM %\tNET I/O\tBLOCK I/O\tPIDS"),
            while True:
                y = 1
                for stat in stats:
                    put_cursor(0, y)
                    y += 1
                    tmp = next(stat)
                    tmp["Id"] = tmp["id"][:12]
                    tmp["Cpu"] = (tmp["cpu_stats"]["cpu_usage"][
                        "total_usage"] / tmp["cpu_stats"]["system_cpu_usage"])
                    tmp["MemUsage"] = humanize.naturalsize(
                        tmp["memory_stats"]["usage"])
                    tmp["Limit"] = humanize.naturalsize(
                        tmp["memory_stats"]["limit"])
                    tmp["Mem"] = (tmp["memory_stats"]["usage"] /
                                  tmp["memory_stats"]["limit"])
                    tmp["NetInput"] = humanize.naturalsize(
                        tmp["networks"]["eth0"]["rx_bytes"])
                    tmp["NetOutput"] = humanize.naturalsize(
                        tmp["networks"]["eth0"]["tx_bytes"])
                    tmp["Pids"] = tmp["pids_stats"]["current"]
                    print pprint_things(pystache.render(self.defaultTemplate, tmp))
        except KeyboardInterrupt:
            put_cursor(0, y)
            colorama.deinit()
            raise KeyboardInterrupt
        put_cursor(0, y)
        colorama.deinit()
        self.settings[self.name] = "\r"

    def final(self):
        return self.settings[self.name]
