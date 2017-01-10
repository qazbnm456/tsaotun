"""This module contains `docker image save` class"""

from .command import Command


class Save(Command):
    """This class implements `docker image save` command"""

    name = "image save"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        image = self.client.get_image(args["image"])
        if args["output"]:
            with open(args["output"], 'w') as f:
                f.write(image.data)
            self.settings[self.name] = "\r"
        else:
            self.settings[self.name] = image.data

    def final(self):
        return self.settings[self.name]
