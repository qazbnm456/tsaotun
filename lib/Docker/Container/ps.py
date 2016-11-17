from .command import Command

class Ps(Command):
    """This class implements `docker ps` command"""

    name = "ps"
    require = []

    TEMPLATE = "ps_template.txt"

    def __init__(self):
        Command.__init__(self)
        self.settings = { "buf": "" }

    def evalCommand(self, args):
        if args["a"]:
            self.settings["buf"] += str(self.client.containers(all=True)) # docker ps -a
        else:
            self.settings["buf"] += str(self.client.containers(all=False)) # docker ps

    def final(self):
        return self.settings
