"""This module contains `docker rmi` class"""

from docker.errors import APIError

from .command import Command


class Rmi(Command):
    """This class implements `docker rmi` command"""

    name = "rmi"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            self.settings[self.name] = args["image"] + "\n"
            self.client.remove_image(**args)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
