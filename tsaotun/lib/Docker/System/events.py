"""This module contains `docker events` class"""

import pystache
import arrow

from .command import Command


class Events(Command):
    """This class implements `docker events` command"""

    name = "events"
    require = []

    defaultTemplate = '{{Time}}\t{{Type}}\t{{Action}}\t{{{Actor}}}'

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["format"] is None:
            fm = self.defaultTemplate
        else:
            fm = args["format"]
        del args["format"]

        args["filters"] = dict(args["filters"]) if args["filters"] else None

        args["decode"] = True
        for event in self.client.events(**args):
            event["Time"] = arrow.get(event["time"])
            print pystache.render(fm, event)
        self.settings[self.name] = ""

    def final(self):
        return self.settings[self.name]
