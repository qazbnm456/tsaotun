"""This module contains `docker network connect` class"""

from .command import Command


def pprint_things(l):
    """Pretty print"""
    return ''.join("{:25}".format(e) for e in l.split("\t")) + "\n"


class Connect(Command):
    """This class implements `docker network connect` command"""

    name = "network connect"
    require = []


    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        self.client.connect_container_to_network(**args)
        self.settings[self.name] = "Done!"

    def final(self):
        return self.settings[self.name]
