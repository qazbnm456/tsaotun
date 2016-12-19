"""This module contains `docker network create` class"""


from docker.types import (IPAMConfig, IPAMPool)
from docker.errors import APIError

from .command import Command


class Create(Command):
    """This class implements `docker network create` command"""

    name = "network create"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def preprocess(self, args):
        """Preprocess arguments provided for `docker network create`"""
        pool = {}

        # subnet
        pool["subnet"] = args["subnet"]
        del args["subnet"]

        # iprange
        pool["iprange"] = args["iprange"]
        del args["iprange"]

        # gateway
        pool["gateway"] = args["gateway"]
        del args["gateway"]

        # create ipam
        ipam_pool = IPAMPool(**pool)
        ipam_config = IPAMConfig(
            driver=args["ipamdriver"],
            pool_configs=[ipam_pool],
            options=dict(args["ipamopt"]) if args["ipamopt"] else None
        )
        del args["ipamdriver"]
        del args["ipamopt"]
        if "None" in str(ipam_config):
            return None
        else:
            return ipam_config

    def eval_command(self, args):
        """Create host config for containers"""
        try:
            args["ipam"] = self.preprocess(args)
            args["labels"] = dict(args["labels"]) if args["labels"] else None
            args["options"] = dict(args["options"]) if args["options"] else None
            self.settings[self.name] = self.client.create_network(**args)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
