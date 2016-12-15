"""This module contains Exec_start class"""

import dockerpty
from docker.errors import APIError

from .command import Command


class Exec_start(Command):
    """This class start a previously set up exec instance"""

    name = "exec_start"
    require = ["exec_create"]

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        """Start a previously set up exec instance"""
        try:
            detach = args["detach"]
            del args["detach"]
            dockerpty.start_exec(
                self.client, self.settings["exec_create"])
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
