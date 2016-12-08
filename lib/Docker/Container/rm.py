"""This module contains `docker rm` class"""

from docker.errors import APIError

from .command import Command

class Rm(Command):
    """This class implements `docker rm` command"""

    name = "rm"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            self.settings[self.name] = args["container"]
            self.client.remove_container(**args)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
