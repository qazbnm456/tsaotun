"""Addon Loader module"""

from os import path
import pkgutil
import imp
from ..Utils.deepgetattr import deepgetattr


class Loader(object):
    """Addon Loader"""

    def __init__(self, addon_path="{}/Tsaotun/addons/".format(path.expanduser("~"))):
        self.__locate(addon_path)

    def __locate(self, addon_path):
        """Locate addon path"""
        if path.exists(addon_path):
            self.addon_path = addon_path
        else:
            raise RuntimeError("addon path not found: {}.".format(addon_path))

    def load(self, tsaotun):
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
            except ImportError as e:
                raise RuntimeError(str(e))

        tsaotun.push(**addons)

    def addons(self):
        """List addons"""
        return [{'Addon': n, 'Enabled': 'true'} for _, n, _ in pkgutil.iter_modules(
            ["{}".format(self.addon_path)])]
