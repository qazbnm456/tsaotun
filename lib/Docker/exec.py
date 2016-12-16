"""This module contains `docker exec` class"""

from .command import Command


class Exec(Command):
    """This class implements `docker exec` command"""

    name = "exec"
    require = ["exec_create", "exec_start"]

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        """Execute a command in a running container"""
        self.settings[self.name] = "\r"

    def final(self):
        return self.settings[self.name]
