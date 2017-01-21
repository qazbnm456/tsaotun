"""Addon Loader module"""

import os
import pkgutil
import imp
from ast import literal_eval
from ConfigParser import RawConfigParser
from git import RemoteProgress

from ..Utils.deepgetattr import deepgetattr
from ..Utils.hightlight import hightlight_python
from ..Utils.urlutil import is_git_url


class Progress(RemoteProgress):
    """Git Progree Handler"""

    def line_dropped(self, line):
        print line

    def update(self, op_code, cur_count, max_count=None, message=''):
        print "{}/{}".format(cur_count, max_count)


class Loader(object):
    """Addon Loader"""
    inspects = {}

    def __init__(self, argparser=None, tsaotun_global_config="{}/Tsaotun/config.ini".format(os.path.expanduser("~")), addon_path="{}/Tsaotun/addons/".format(os.path.expanduser("~"))):
        self.argparser = argparser
        self.__locate(addon_path)
        try:
            if not os.path.exists(tsaotun_global_config):
                open(tsaotun_global_config, 'a').close()
            self.tsaotun_global_config = tsaotun_global_config
        except OSError as e:
            raise RuntimeError(
                "{}".format(str(e)))

    def __locate(self, addon_path):
        """Locate addon path"""
        try:
            if not os.path.exists(addon_path):
                os.makedirs(addon_path)
            self.addon_path = addon_path
        except OSError as e:
            raise RuntimeError(
                "{}".format(str(e)))

    def __parse_args(self, configs):
        """Parsing __argparse__ and assign to argparser"""
        if self.argparser:
            for config in configs:
                if config["position"] == 'Self':
                    parser = self.argparser[
                        config["namespace"]][config["position"]]
                    for action in config["actions"]:
                        exec("import textwrap; parser.{}".format(action), {'parser': parser})
                    self.argparser[config["namespace"]][
                        config["position"]] = parser
                else:
                    if config["subcommand"]:
                        parser = self.argparser[config["namespace"]][
                            config["position"]].choices.get(config["subcommand"])
                        for action in config["actions"]:
                            exec("import textwrap; parser.{}".format(action), {'parser': parser})
                        self.argparser[config["namespace"]][
                            config["position"]].choices.update({config["subcommand"]: parser})
                    else:
                        parser = self.argparser[
                            config["namespace"]][config["position"]]
                        subparser = None
                        for i, action in enumerate(config["actions"]):
                            if i == 0:
                                exec(
                                    "import textwrap; import argparse; global subparser; subparser = parser.{}".format(action))
                            else:
                                exec("import textwrap; global subparser; subparser.{}".format(action))
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

    def install(self, url, addon):
        """Install an addon from a given url"""
        if is_git_url(url):
            from git import (Repo, GitCommandError)
            if addon is None:
                addon = url.split('/')[-1].split('.')[0]
            dest = os.path.join(self.addon_path, addon)
            try:
                Repo.clone_from(url, dest, progress=Progress())
                if 'requirements.txt' in os.listdir(dest):
                    os.system('pip install -r requirements.txt')
                return "'{}' successfully installed!".format(addon)
            except GitCommandError as e:
                raise RuntimeError("{}".format(str(e)))
            except IOError:
                print "Please run 'pip install -r {}' to install the needed requirements, and the installation of {} is done.".format(os.path.join(dest, 'requirements.txt'), addon)
        else:
            raise RuntimeError("Invalid URL: {}".format(url))

    def rm(self, addon):
        """Remove an addon"""
        import shutil
        try:
            shutil.rmtree(os.path.join(self.addon_path, addon))
            return "'{}' successfully removed!".format(addon)
        except OSError as e:
            raise RuntimeError("{}".format(str(e)))

    def addons(self):
        """List addons"""
        addon_names = [n for _, n, _ in pkgutil.iter_modules(
            ["{}".format(self.addon_path)])]
        return [{'Addon': n, 'Enabled': a} for n, a in zip(addon_names, self.__active(addon_names))]
