import platform
import os
import re
import time
import json

from docker import Client
from docker.errors import APIError, NullResource, NotFound

from ..Utils import (logger, shell_escape, switch)

try:
    import urlparse
except ImportError:  # For Python 3
    import urllib.parse as urlparse

nonspace = re.compile(r'\S')


def jsoniterparse(j):
    decoder = json.JSONDecoder()
    pos = 0
    while True:
        matched = nonspace.search(j, pos)
        if not matched:
            break
        pos = matched.start()
        decoded, pos = decoder.raw_decode(j, pos)
        yield decoded


class time_limit(object):

    def __init__(self, seconds):
        self.seconds = seconds

    def __enter__(self):
        self.die_after = time.time() + self.seconds
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def timed_reset(self):
        self.die_after = time.time() + self.seconds

    @property
    def timed_out(self):
        return time.time() > self.die_after


class Docker(object):
    """Class for manipulating the docker client."""

    host = None
    client = None
    ctr = None
    current_ctr = None
    buf = dict()

    def __init__(self):
        """Loading docker environments"""
        if platform.system() == 'Darwin' or platform.system() == 'Windows':
            try:
                # TLS problem, can be referenced from
                # https://github.com/docker/machine/issues/1335
                from docker.utils import kwargs_from_env
                self.host = '{0}'.format(urlparse.urlparse(
                    os.environ['DOCKER_HOST']).netloc.split(':')[0])
                self.client = Client(
                    base_url='{0}'.format(os.environ['DOCKER_HOST']))
                kwargs = kwargs_from_env()
                kwargs['tls'].assert_hostname = False
                self.client = Client(**kwargs)
            except KeyError:
                self.host = '127.0.0.1'
                self.client = Client(base_url='unix://var/run/docker.sock')
        else:
            self.host = '127.0.0.1'
            self.client = Client(base_url='unix://var/run/docker.sock')

    def dry(self):
        """Load the command and configure the environment with dry-run"""
        self.buf = "dry-run complete"

    def load(self, args):
        """Load the command_flag and configure the environment"""
        command_flag = args["command_flag"]
        del args["command_flag"]
        mod = __import__("Container." + command_flag,
                         globals(), locals(), ['dummy'], -1)
        mod_instance = getattr(mod, command_flag.capitalize())()

        if mod_instance.require:
            mod_instance.load_require(args, self.client)

        self.buf = mod_instance.command(args, self.client)

    def recv(self):
        """Receive outcome"""
        return self.buf
