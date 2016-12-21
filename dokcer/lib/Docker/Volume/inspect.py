"""This module contains `docker volume inspect` class"""

import json
import pystache
from docker.errors import APIError

from .command import Command


class Inspect(Command):
    """This class implements `docker volume inspect` command"""

    name = "volume inspect"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            Volumes = []
            volumes = args["volumes"]
            del args["volumes"]
            for Volume in volumes:
                if args["format"]:
                    Volumes.append(pystache.render(
                        args["format"], self.client.inspect_volume(Volume)))
                else:
                    Volumes.append(json.dumps(
                        self.client.inspect_volume(Volume), indent=4))
            self.settings[self.name] = '\n'.join(Volumes)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
