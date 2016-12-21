"""This module contains base class of `docker volume command` class"""

from abc import ABCMeta, abstractmethod
from six import with_metaclass


class Command(with_metaclass(ABCMeta, object)):
    """
    This class represents a command, it must be extended
    for any class which implements a type of command
    """

    name = "command"
    client = None
    require = []
    settings = {}

    @abstractmethod
    def eval_command(self, args):
        """Evalute the command"""
        pass

    def final(self):
        """Do the final job"""
        return self.settings

    def load_require(self, args, client):
        """Load require dependencies"""
        for command in self.require:
            mod = __import__(command,
                             globals(), locals(), ['dummy'], -1)
            mod_instance = getattr(mod, command.capitalize())()
            self.settings[command] = mod_instance.command(args, client)
            del mod

    def command(self, args, client):
        """Command class entrypoint"""
        self.client = client
        self.eval_command(args)
        return self.final()
