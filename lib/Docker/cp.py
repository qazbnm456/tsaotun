"""This module contains `docker cp` class"""

import os
import sys
import tempfile
import tarfile
from enum import Enum
from docker.errors import APIError
from ..Utils import switch

from .command import Command


Direction = Enum(
    'Direction', 'fromContainer toContainer acrossContainers', start=0)


class Cp(Command):
    """This class implements `docker cp` command"""

    name = "cp"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def split_cp_arg(self, arg):
        """Split provided cp arguments"""
        if os.path.isabs(arg):
            return "", arg

        parts = arg.split(':', 2)

        if (len(parts) == 1) or (parts[0][0] == '.'):
            return "", arg
        else:
            return parts[0], parts[1]

    def copy_from_container(self, args, src_container, src_path, dst_path):
        """Preprocess arguments and tarfile provided for `docker cp`"""
        args['container'] = src_container
        args['path'] = src_path
        tar, stat = self.client.get_archive(**args)
        if dst_path == '-':
            self.settings[self.name] = tar.read()
        else:
            fd = tempfile.NamedTemporaryFile(delete=False)
            fd.write(tar.read())
            fd.close()
            with tarfile.open(fd.name, 'r') as t:
                t.extractall(path=dst_path)
            os.unlink(fd.name)
            self.settings[self.name] = stat

    def copy_to_container(self, args, src_path, dst_container, dst_path):
        """Preprocess arguments and tarfile provided for `docker cp`"""
        args['container'] = dst_container
        args['path'] = dst_path
        if src_path == '-':
            args['data'] = sys.stdin.read()
            if self.client.put_archive(**args):
                self.settings[self.name] = "Done!"
            else:
                self.settings[self.name] = "Failed!"
        else:
            fd = tempfile.NamedTemporaryFile(delete=False)
            with tarfile.open(fd.name, 'w') as t:
                t.add(src_path, os.path.basename(src_path))
            fd.close()
            with open(fd.name, 'rb') as f:
                args['data'] = f.read()
                if self.client.put_archive(**args):
                    self.settings[self.name] = "Done!"
                else:
                    self.settings[self.name] = "Failed!"
            os.unlink(fd.name)

    def eval_command(self, args):
        try:
            direction = 0
            src_container, src_path = self.split_cp_arg(args['src'])
            dst_container, dst_path = self.split_cp_arg(args['dest'])
            del args['src']
            del args['dest']

            if src_container != '':
                direction |= Direction.fromContainer.value
            if dst_container != '':
                direction |= Direction.toContainer.value

            for case in switch.switch(direction):
                if case(Direction.fromContainer.value):
                    self.copy_from_container(
                        args, src_container, src_path, dst_path)
                    break
                if case(Direction.toContainer.value):
                    self.copy_to_container(
                        args, src_path, dst_container, dst_path)
                    break
                if case(Direction.acrossContainers.value):
                    self.settings[
                        self.name] = "copying between containers is not supported"
                    break
                if case():
                    self.settings[
                        self.name] = "must specify at least one container source"
        except (APIError, AttributeError, ValueError) as e:
            raise e

    def final(self):
        return self.settings[self.name]
