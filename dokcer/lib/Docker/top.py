"""This module contains `docker top` class"""

import pystache
from pytabwriter import TabWriter

from .command import Command


class Top(Command):
    """This class implements `docker top` command"""

    name = "top"
    require = []

    defaultTemplate = '{{Pid}}\t{{User}}\t{{Time}}\t{{{Command}}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        tw = TabWriter()
        tw.padding = [8, 8, 8]
        tw.writeln(
            "PID\tUSER\tTime\tCOMMAND")
        infos = self.client.top(**args)
        if infos:
            for info in infos["Processes"]:
                process = {}
                process["Pid"] = info[0]
                process["User"] = info[1]
                process["Time"] = info[2]
                process["Command"] = info[3]
                tw.writeln(pystache.render(self.defaultTemplate, process))
        self.settings[self.name] = str(tw)

    def final(self):
        return self.settings[self.name]
