"""Addon Loader module"""

from os import path
import pkgutil
import imp
from ast import literal_eval
from ConfigParser import RawConfigParser

from ..Utils.deepgetattr import deepgetattr
from ..Utils.hightlight import hightlight_python


class Loader(object):
    """Addon Loader"""
    inspects = {}

    def __init__(self, argparser=None, tsaotun_global_config="{}/Tsaotun/config.ini".format(path.expanduser("~")), addon_path="{}/Tsaotun/addons/".format(path.expanduser("~"))):
        self.argparser = argparser
        self.__locate(addon_path)
        if path.exists(tsaotun_global_config):
            self.tsaotun_global_config = tsaotun_global_config
        else:
            raise RuntimeError(
                "global config file is not found: {}.".format(tsaotun_global_config))

    def __locate(self, addon_path):
        """Locate addon path"""
        if path.exists(addon_path):
            self.addon_path = addon_path
        else:
            raise RuntimeError(
                "addon path is not found: {}.".format(addon_path))

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
                                exec(
                                    "import argparse; global subparser; subparser = parser.{}".format(action))
                            else:
                                exec("global subparser; subparser.{}".format(action))
                        self.argparser[config["namespace"]][
                            config["position"]] = parser
        else:
            raise RuntimeError("argparser is not specified.")

    def __parse_config(self, section, options=None):
        """Parsing global config file"""
        cfg = RawConfigParser()
        with open(self.tsaotun_global_config) as f:
            cfg.readfp(f, self.tsaotun_global_config)
        if cfg.has_section(section) is False:
            cfg.add_section(section)
        if options:
            stored = [cfg.get(section, option) if cfg.has_option(section, option) else cfg.set(
                section, option, 'False') is True for option in options]
        else:
            stored = cfg.items(section)
        with open(self.tsaotun_global_config, 'wb') as f:
            cfg.write(f)
        return stored

    def __active(self, addon_names):
        """Check if the given addon is active"""
        return self.__parse_config('addon', addon_names)

    def load(self):
        """Load addons"""
        addon_names = [n for _, n, _ in pkgutil.iter_modules(
            ["{}".format(self.addon_path)])]
        addons = {}
        for addon_name, active in zip(addon_names, self.__active(addon_names)):
            try:
                f, filename, description = imp.find_module(
                    addon_name, [self.addon_path])
                mod = imp.load_module(
                    addon_name, f, filename, description)
                self.inspects[addon_name] = ''.join(
                    [mod.__file__.split('.')[0], '.py'])
                if literal_eval(active):
                    for k, v in mod.__override__.iteritems():
                        addons["{}|{}".format(k, v)] = deepgetattr(
                            mod, "{}.{}".format(k, v))
                    self.__parse_args(mod.__argparse__)
            except ImportError as e:
                raise RuntimeError(str(e))

        return addons, self.argparser

    def enable(self, addon):
        """Enable an addon"""
        try:
            if self.inspects[addon]:
                cfg = RawConfigParser()
                with open(self.tsaotun_global_config) as f:
                    cfg.readfp(f, self.tsaotun_global_config)
                cfg.set('addon', addon, 'True')
                with open(self.tsaotun_global_config, 'wb') as f:
                    cfg.write(f)
                return "Done!"
        except KeyError as e:
            raise RuntimeError("No such addon: {}".format(str(e)))

    def disable(self, addon):
        """Disable an addon"""
        try:
            if self.inspects[addon]:
                cfg = RawConfigParser()
                with open(self.tsaotun_global_config) as f:
                    cfg.readfp(f, self.tsaotun_global_config)
                cfg.set('addon', addon, 'False')
                with open(self.tsaotun_global_config, 'wb') as f:
                    cfg.write(f)
                return "Done!"
        except KeyError as e:
            raise RuntimeError("No such addon: {}".format(str(e)))

    def inspect(self, addon):
        """Inspect an addon"""
        try:
            args = {'sourcefile': self.inspects[addon]}
            return hightlight_python(args)
        except KeyError as e:
            raise RuntimeError("No such addon: {}".format(str(e)))

    def addons(self):
        """List addons"""
        addon_names = [n for _, n, _ in pkgutil.iter_modules(
            ["{}".format(self.addon_path)])]
        return [{'Addon': n, 'Enabled': a} for n, a in zip(addon_names, self.__active(addon_names))]
