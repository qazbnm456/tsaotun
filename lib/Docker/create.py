"""This module contains `docker create` class"""

import time
from hashlib import sha1
from docker.errors import APIError

from .command import Command


class Create(Command):
    """This class implements `docker create` command"""

    name = "create"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def preprocess(self, args):
        """Preprocess arguments provided for `docker create`"""
        # port_bindings
        if args.get("port_bindings"):
            tmp = args["port_bindings"]
            args["port_bindings"] = dict([tmp.strip('{}').split(':'), ])

        # image
        image = args["image"][0]
        del args["image"]

        # name
        if "name" in args:
            name = args["name"]
            del args["name"]
        else:
            name = sha1(str(time.clock())).hexdigest()

        # detach
        detach = args["detach"]
        del args["detach"]

        # tty
        tty = args["tty"]
        del args["tty"]

        # stdin_open
        stdin_open = args["stdin_open"]
        del args["stdin_open"]

        # command
        if "command" in args:
            command = args["command"]
            del args["command"]

        # create host_config
        host_config = self.client.create_host_config(**args)

        # store back arguments
        del args["port_bindings"]
        args["host_config"] = host_config
        args["image"] = image
        args["name"] = name
        args["detach"] = detach
        args["tty"] = tty
        args["stdin_open"] = stdin_open
        args["command"] = command

    def eval_command(self, args):
        """Create host config for containers"""
        try:
            self.preprocess(args)
            self.settings[self.name] = self.client.create_container(**args)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
