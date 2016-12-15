"""This module contains `docker restart` class"""

from docker.errors import APIError

from .command import Command


class Restart(Command):
    """This class implements `docker restart` command"""

    name = "restart"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            Ids = []
            containers = args["containers"]
            del args["containers"]
            for Id in containers:
                Ids.append(Id)
                args['container'] = Id
                self.client.restart(**args)
                del args['container']
            self.settings[self.name] = '\n'.join(Ids)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
