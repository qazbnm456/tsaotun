"""This module contains `docker ps` class"""

from .command import Command

class Ps(Command):
    """This class implements `docker ps` command"""

    name = "ps"
    require = []

    TEMPLATE = "ps_template.txt"

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        self.settings[self.name] = self.client.containers(**args)

    def final(self):
        return self.settings[self.name]
