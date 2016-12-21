"""This module contains `docker volume create` class"""


from docker.errors import APIError

from .command import Command


class Create(Command):
    """This class implements `docker volume create` command"""

    name = "volume create"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        """Create host config for containers"""
        try:
            args["driver_opts"] = dict(args["driver_opts"]) if args["driver_opts"] else None
            args["labels"] = dict(args["labels"]) if args["labels"] else None
            self.settings[self.name] = self.client.create_volume(**args)["Name"]
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
