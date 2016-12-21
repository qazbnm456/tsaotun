"""This module contains `docker top` class"""

import pystache

from .command import Command


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:20}".format(e) for e in l.split("\t")) + "\n"


class Top(Command):
    """This class implements `docker top` command"""

    name = "top"
    require = []

    defaultTemplate = '{{Pid}}\t{{User}}\t{{Time}}\t{{{Command}}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        self.settings[self.name] = pprint_things(
            "PID\tUSER\tTime\tCOMMAND")
        infos = self.client.top(**args)
        for info in infos["Processes"]:
            process = {}
            process["Pid"] = info[0]
            process["User"] = info[1]
            process["Time"] = info[2]
            process["Command"] = info[3]
            self.settings[
                self.name] += pprint_things(pystache.render(self.defaultTemplate, process))

    def final(self):
        return self.settings[self.name]
