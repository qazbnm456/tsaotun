"""This module contains `docker image build` class"""

import sys
from io import BytesIO

from .command import Command
from ...Utils.json_iterparse import json_iterparse
from ...Utils.switch import switch
from ...Utils.urlutil import (is_git_url, is_url)


class Build(Command):
    """This class implements `docker image build` command"""

    name = "image build"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def preprocess(self, args):
        """Preprocess build arguments"""
        for case in switch(args["path"]):
            if case('-'):
                del args["path"]
                args['fileobj'] = BytesIO(sys.stdin.read())
                break
            if is_git_url(args["path"]):
                break
            if is_url(args["path"]):
                break
            if case():
                break
        args["buildargs"] = dict(args["buildargs"]) if args[
            "buildargs"] else None
        args["container_limits"] = {
            "memory": args["mem_limit"],
            "memswap": args["memswap_limit"],
            "cpushares": args["cpu_shares"],
            "cpusetcpus": args["cpuset_cpus"],
        }
        del args["mem_limit"]
        del args["memswap_limit"]
        del args["cpu_shares"]
        del args["cpuset_cpus"]

        # following options are not supported right now
        del args["cachefrom"]
        del args["cgroup_parent"]
        del args["cpu_period"]
        del args["cpu_quota"]
        del args["cpuset_mems"]

        args["labels"] = dict(args["labels"]) if args[
            "labels"] else None
        args["shmsize"] = 67108864

    def eval_command(self, args):
        self.preprocess(args)
        for line in self.client.build(**args):
            for iterElement in list(json_iterparse(line)):
                print iterElement["stream"],
        self.settings[self.name] = ""

    def final(self):
        return self.settings[self.name]
