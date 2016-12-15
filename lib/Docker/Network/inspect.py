"""This module contains `docker network inspect` class"""

import json
from docker.errors import APIError

from .command import Command


class Inspect(Command):
    """This class implements `docker network inspect` command"""

    name = "network inspect"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            Networks = []
            networks = args["networks"]
            del args["networks"]
            for Network in networks:
                Networks.append(json.dumps(
                    self.client.inspect_network(Network), indent=4))
            self.settings[self.name] = '\n'.join(Networks)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
