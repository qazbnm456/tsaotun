"""This module contains `docker start` class"""

import dockerpty

from .command import Command


class Start(Command):
    """This class implements `docker start` command"""

    name = "start"
    require = ["create"]

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        """Start containers"""
        if (args["detach"] is False) and (args["tty"]):
            dockerpty.start(self.client, self.settings["create"])
        else:
            self.client.start(self.settings["create"])

    def final(self):
        return self.settings[self.name]
