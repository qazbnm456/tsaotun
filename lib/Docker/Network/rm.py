"""This module contains `docker network rm` class"""

from docker.errors import APIError

from .command import Command


class Rm(Command):
    """This class implements `docker network rm` command"""

    name = "network rm"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            Ids = []
            networks = args["networks"]
            del args["networks"]
            for Id in networks:
                Ids.append(Id)
                self.client.remove_network(Id)
            self.settings[self.name] = '\n'.join(Ids)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
