"""This module contains ExecCreate class"""


from docker.errors import APIError

from .command import Command


class ExecCreate(Command):
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
            self.settings[self.name] = self.client.exec_create(**args)
            args["detach"] = detach
            del args["stdin_open"]
            del args["cmd"]
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
