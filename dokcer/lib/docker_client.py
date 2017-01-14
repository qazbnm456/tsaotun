"""This module contains Docker class"""

import platform
import os

from docker import APIClient

try:
    import urlparse
except ImportError:  # For Python 3
    import urllib.parse as urlparse


class Docker(object):
    """Class for manipulating the docker client."""

    __stack = None

    host = None
    client = None
    ctr = None
    current_ctr = None
    buf = None

    category = None
    command_flag = None

    def __init__(self, host='127.0.0.1'):
        """Loading docker environments"""
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            try:
                # TLS problem, can be referenced from
                # https://github.com/docker/machine/issues/1335
                from docker.utils import kwargs_from_env
                self.host = '{0}'.format(urlparse.urlparse(
                    os.environ['DOCKER_HOST']).netloc.split(':')[0])
                self.client = APIClient(
                    base_url='{0}'.format(os.environ['DOCKER_HOST']))
                kwargs = kwargs_from_env()
                kwargs['tls'].assert_hostname = False
                self.client = APIClient(**kwargs)
            except KeyError:
                self.host = host
                self.client = APIClient(base_url='unix://var/run/docker.sock')
        else:
            self.host = host
            self.client = APIClient(base_url='unix://var/run/docker.sock')
        self.client.ping()

    def __dry(self):
        """Load the command and configure the environment with dry-run"""
        self.buf = "dry-run complete"

    def load(self, args, dry=False):
        """Load the command_flag and configure the environment"""
        if dry:
            self.__dry()
        else:
            self.category = args["manage_flag"]
            del args["manage_flag"]
            if args.get("{}_flag".format(self.category)):
                self.command_flag = args["{}_flag".format(self.category)]
                del args["{}_flag".format(self.category)]
            else:
                self.command_flag = self.category
                self.category = 'system'
            mod = __import__("Docker.{}.{}".format(self.category.capitalize(), self.command_flag),
                             globals(), locals(), ['dummy'], -1)
            self.__intrude(mod)
            mod_instance = getattr(mod, self.command_flag.capitalize())()

            if mod_instance.require:
                mod_instance.load_require(args, self.client)

            self.buf = mod_instance.command(args, self.client)

    def buffer(self):
        """Receive outcome"""
        return self.buf

    def set_buffer(self, buf):
        """Set received outcome"""
        self.buf = buf

    def push(self, **kwargs):
        """Push custom classes into Docker.__stack"""
        self.__stack = kwargs

    def __intrude(self, mod):
        """Intrude classes"""
        if self.__stack:
            for k, v in self.__stack.iteritems():
                override, value = k.split('|')
                if "dokcer.lib.Docker." + override == mod.__name__:
                    setattr(mod, value, v)
