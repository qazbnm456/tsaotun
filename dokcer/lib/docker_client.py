"""This module contains Docker class"""

import platform
import os
import re
import json

from docker import APIClient

try:
    import urlparse
except ImportError:  # For Python 3
    import urllib.parse as urlparse

nonspace = re.compile(r'\S')


def jsoniterparse(j):
    """This method implements iterative json parsing"""
    decoder = json.JSONDecoder()
    pos = 0
    while True:
        matched = nonspace.search(j, pos)
        if not matched:
            break
        pos = matched.start()
        decoded, pos = decoder.raw_decode(j, pos)
        yield decoded


class Docker(object):
    """Class for manipulating the docker client."""

    __stack = None

    host = None
    client = None
    ctr = None
    current_ctr = None
    buf = dict()

    category = None
    command_flag = None

    def __init__(self):
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
                self.host = '127.0.0.1'
                self.client = APIClient(base_url='unix://var/run/docker.sock')
        else:
            self.host = '127.0.0.1'
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
            if "network_flag" in args:
                self.category = "{}.".format(args["command_flag"])
                self.command_flag = args["network_flag"]
                del args["network_flag"]
            elif "volume_flag" in args:
                self.category = "{}.".format(args["command_flag"])
                self.command_flag = args["volume_flag"]
                del args["volume_flag"]
            else:
                self.category = ""
                self.command_flag = args["command_flag"]
            del args["command_flag"]
            mod = __import__("Docker.{}{}".format(self.category.capitalize(), self.command_flag),
                             globals(), locals(), ['dummy'], -1)
            self.__intrude(mod)
            mod_instance = getattr(mod, self.command_flag.capitalize())()

            if mod_instance.require:
                mod_instance.load_require(args, self.client)

            self.buf = mod_instance.command(args, self.client)

    def recv(self):
        """Receive outcome"""
        return self.buf

    def set_recv(self, buf):
        """Set received outcome"""
        self.buf = buf

    def push(self, **kwargs):
        """Push custom classes into Docker.__stack"""
        self.__stack = kwargs

    def __intrude(self, mod):
        """Intrude classes"""
        if self.__stack:
            for k, v in self.__stack.iteritems():
                setattr(mod, k.capitalize(), v)
