"""This module contains `docker pull` class"""

import colorama

from .command import Command
from ..Utils import (json_iterparse)


colorama.init()
info = {
    "title": "",
    "layers": {},
    "final": []
}
MINY, OFFSET = 1, 2

def put_cursor(x, y):
    print "\x1b[{};{}H".format(y + 1, x + 1)


def clear():
    print "\x1b[2J"


class Pull(Command):
    """This class implements `docker pull` command"""

    name = "pull"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def preprocess(self, args):
        try:
            repository, tag = args["image"][0].split(':', 2)
        except ValueError:
            repository, tag = args["image"][0], None
        del args["image"]
        args["repository"] = repository
        if tag:
            args["tag"] = tag
        else:
            args["tag"] = "latest"
        args["stream"] = True

    def output(self, infos, args):
        try:
            if infos["id"] == args["tag"]:
                info["title"] = "{}: {}".format(infos["id"], infos["status"])
            elif "Pulling" in infos["status"]:
                info["layers"][infos["id"]] = {"status": infos[
                    "status"], "progressDetail": infos["progressDetail"]}
            else:
                for infos_key in infos.keys():
                    for info_key in info["layers"][infos["id"]]:
                        if infos_key == info_key:
                            info["layers"][infos["id"]][
                                info_key] = infos[infos_key]
                            del infos[infos_key]
                for infos_key in infos.keys():
                    if infos_key != "id":
                        info["layers"][infos["id"]][
                            infos_key] = infos[infos_key]
                clear()
                put_cursor(0, MINY)
                s = '\n'.join(["%s: %s: %s" % (info_key, info["layers"][info_key]["status"], info[
                              "layers"][info_key]["progressDetail"]) for info_key in info["layers"].keys()])
                line_n = len(s.split('\n'))
                print "%s\n%s" % (info["title"], s)
                return line_n
        except KeyError:
            if len(info["final"]):
                info["final"].append(infos["status"])
                clear()
                put_cursor(0, MINY)
                s = '\n'.join(info["final"])
                line_n = len(s.split('\n'))
                print "%s\n%s" % (info["title"], s)
                return line_n
            else:
                info["final"].append(infos["status"])

    def eval_command(self, args):
        self.preprocess(args)
        line_n = 0
        try:
            for line in self.client.pull(**args):
                for iterElement in list(json_iterparse.json_iterparse(line)):
                    line_n = self.output(iterElement, args)
        except KeyboardInterrupt:
            put_cursor(0, MINY + OFFSET + line_n)
            colorama.deinit()
            raise KeyboardInterrupt
        put_cursor(0, MINY + OFFSET + line_n)
        colorama.deinit()
        self.settings[self.name] = "\r"

    def final(self):
        return self.settings[self.name]
