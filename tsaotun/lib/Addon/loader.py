"""Addon Loader module"""

from os import path
import pkgutil
import imp
from ..Utils.deepgetattr import deepgetattr


class Loader(object):
    """Addon Loader"""

    def __init__(self, argparser=None, addon_path="{}/Tsaotun/addons/".format(path.expanduser("~"))):
        self.__locate(addon_path)
        self.argparser = argparser

    def __locate(self, addon_path):
        """Locate addon path"""
        if path.exists(addon_path):
            self.addon_path = addon_path
        else:
            raise RuntimeError("addon path not found: {}.".format(addon_path))

    def __parse_args(self, configs):
        """Parsing __argparse__ and assign to argparser"""
        if self.argparser:
            for config in configs:
                if config["position"] == 'Self':
                    parser = self.argparser[
                        config["namespace"]][config["position"]]
                    for action in config["actions"]:
                        exec("parser.{}".format(action), {'parser': parser})
                    self.argparser[config["namespace"]][
                        config["position"]] = parser
                else:
                    if config["subcommand"]:
                        parser = self.argparser[config["namespace"]][
                            config["position"]].choices.get(config["subcommand"])
                        for action in config["actions"]:
                            exec("parser.{}".format(action), {'parser': parser})
                        self.argparser[config["namespace"]][
                            config["position"]].choices.update({config["subcommand"]: parser})
                    else:
                        parser = self.argparser[
                            config["namespace"]][config["position"]]
                        subparser = None
                        for i, action in enumerate(config["actions"]):
                            if i == 0:
                                exec("import argparse; global subparser; subparser = parser.{}".format(action))
                            else:
                                exec("global subparser; subparser.{}".format(action))
                        self.argparser[config["namespace"]][
                            config["position"]] = parser
        else:
            raise RuntimeError("argparser is not specified.")

    def load(self):
        """Load addons"""
        addon_names = [n for _, n, _ in pkgutil.iter_modules(
            ["{}".format(self.addon_path)])]
        addons = {}
        for addon_name in addon_names:
            try:
                f, filename, description = imp.find_module(
                    addon_name, [self.addon_path])
                mod = imp.load_module(
                    addon_name, f, filename, description)
                for k, v in mod.__override__.iteritems():
                    addons["{}|{}".format(k, v)] = deepgetattr(
                        mod, "{}.{}".format(k, v))
                self.__parse_args(mod.__argparse__)
            except ImportError as e:
                raise RuntimeError(str(e))

        return addons, self.argparser

    def addons(self):
        """List addons"""
        return [{'Addon': n, 'Enabled': 'true'} for _, n, _ in pkgutil.iter_modules(
            ["{}".format(self.addon_path)])]
