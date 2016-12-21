"""This module contains `docker run` class"""

from .command import Command


class Run(Command):
    """This class implements `docker run` command"""

    name = "run"
    require = ["create", "start"]

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        if args["detach"] is False and not args["tty"]:
            for line in self.client.logs(
                    self.settings["create"], stream=True):
                print line,
            self.settings[self.name] = "\r"
        else:
            self.settings[self.name] = self.settings["create"]["Id"]

    def final(self):
        return self.settings
