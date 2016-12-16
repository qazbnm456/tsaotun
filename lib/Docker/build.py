"""This module contains `docker build` class"""

import sys
from io import BytesIO

from .command import Command
from ..Utils import (json_iterparse, switch, urlutil)


class Build(Command):
    """This class implements `docker build` command"""

    name = "build"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def preprocess(self, args):
        for case in switch.switch(args["path"]):
            if case('-'):
                del args["path"]
                args['fileobj'] = BytesIO(sys.stdin.read())
                break
            if urlutil.is_git_url(args["path"]):
                break
            if urlutil.is_url(args["path"]):
                break
            if case():
                break

    def eval_command(self, args):
        self.preprocess(args)
        for line in self.client.build(**args):
            for iterElement in list(json_iterparse.json_iterparse(line)):
                print iterElement["stream"],
        self.settings[self.name] = ""

    def final(self):
        return self.settings[self.name]
