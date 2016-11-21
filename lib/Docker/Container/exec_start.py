"""This module contains ExecStart class"""


from docker.errors import APIError

from .command import Command


class ExecStart(Command):
    """This class start a previously set up exec instance"""

    name = "exec_start"
    require = ["exec_create"]

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        """Start a previously set up exec instance"""
        try:
            args["exec_id"] = self.settings["exec_create"]
            self.settings[self.name] = self.client.exec_start(**args)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
