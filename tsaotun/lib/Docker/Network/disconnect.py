"""This module contains `docker network disconnect` class"""

from .command import Command


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:25}".format(e) for e in l.split("\t")) + "\n"


class Disconnect(Command):
    """This class implements `docker network disconnect` command"""

    name = "network disconnect"
    require = []


    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        self.client.disconnect_container_from_network(**args)
        self.settings[self.name] = "Done!"

    def final(self):
        return self.settings[self.name]
