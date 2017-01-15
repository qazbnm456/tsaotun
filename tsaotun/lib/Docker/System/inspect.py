"""This module contains `docker inspect` class"""

import json
import pystache
from docker.errors import APIError

from .command import Command


class Inspect(Command):
    """This class implements `docker inspect` command"""

    name = "inspect"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            obj = args["object"]
            del args["object"]
            try:
                if args["format"]:
                    self.settings[self.name] = pystache.render(args["format"], self.client.inspect_container(obj))
                else:
                    self.settings[self.name] = json.dumps(
                        self.client.inspect_container(obj), indent=4) + "\n"
            except APIError as e:
                if "No such container" in str(e):
                    try:
                        if args["format"]:
                            self.settings[self.name] = pystache.render(args["format"], self.client.inspect_image(obj))
                        else:
                            self.settings[self.name] = json.dumps(
                                self.client.inspect_image(obj), indent=4) + "\n"
                    except APIError as ev:
                        raise ev
                else:
                    raise e
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
