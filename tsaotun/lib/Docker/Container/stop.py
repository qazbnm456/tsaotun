"""This module contains `docker container stop` class"""

from docker.errors import APIError

from .command import Command


class Stop(Command):
    """This class implements `docker container stop` command"""

    name = "container stop"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        """Stop containers"""
        try:
            Ids = []
            containers = args["containers"]
            del args["containers"]
            for Id in containers:
                Ids.append(Id)
                args['container'] = Id
                self.client.stop(**args)
                del args['container']
            self.settings[self.name] = '\n'.join(Ids)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
