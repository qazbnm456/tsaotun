"""This module contains Exec_create class"""

import dockerpty
from docker.errors import APIError

from .command import Command


class Exec_create(Command):
    """This class sets up an exec instance in a running container"""

    name = "exec_create"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        """Set up an exec instance in a running container"""
        try:
            detach = args["detach"]
            del args["detach"]
            stdin_open = args["stdin_open"]
            del args["stdin_open"]
            self.settings[self.name] = dockerpty.exec_create(self.client, args["container"], args["cmd"], interactive=stdin_open)
            args["detach"] = detach
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
