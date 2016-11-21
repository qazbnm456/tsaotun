"""This module contains `docker rm` class"""

from docker.errors import APIError

from .command import Command

class Rm(Command):
    """This class implements `docker rm` command"""

    name = "rm"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            if args["container"] == 0:
                if "run" in self.settings:
                    args["container"] = self.settings[self.name] = self.settings["run"]
                    self.client.remove_container(**args)
                else:
                    self.settings[self.name] = "No containers existed!"
            else:
                self.settings[self.name] = args["container"]
                self.client.remove_container(**args)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
