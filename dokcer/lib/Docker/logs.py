"""This module contains `docker logs` class"""

from .command import Command


class Logs(Command):
    """This class implements `docker logs` command"""

    name = "logs"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        self.settings[self.name] = self.client.logs(**args) if self.client.logs(**args) else "\r"

    def final(self):
        return self.settings[self.name]
