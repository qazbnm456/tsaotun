"""This module contains `docker rmi` class"""

from docker.errors import APIError

from .command import Command


class Rmi(Command):
    """This class implements `docker rmi` command"""

    name = "rmi"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            Images = []
            images = args['images']
            del args['images']
            for Image in images:
                Images.append(Image)
                args['image'] = Image
                self.client.remove_image(**args)
                del args['image']
            self.settings[self.name] = '\n'.join(Images)
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
