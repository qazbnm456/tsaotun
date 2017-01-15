"""This module contains `docker version` class"""

from platform import python_version, system, machine
import pystache
import arrow
from .... import __version__

from .command import Command


class Version(Command):
    """This class implements `docker version` command"""

    name = "version"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        versions = self.client.version()
        versions["ClientVersion"] = __version__
        versions["PythonVersion"] = python_version()
        versions["ClientOs"] = system()
        versions["ClientArch"] = machine()
        versions["BuildTime"] = arrow.get(versions["BuildTime"]).humanize()

        self.settings[self.name] = pystache.render("""\
Client:
    Version:         {{ClientVersion}}
    Python version:  {{PythonVersion}}
    OS/Arch:         {{ClientOs}}/{{ClientArch}}

Server:
    Version:         {{Version}}
    API version:     {{ApiVersion}} (minimum version {{MinAPIVersion}})
    Go version:      {{GoVersion}}
    Git commit:      {{GitCommit}}
    Built:           {{BuildTime}}
    OS/Arch:         {{Os}}/{{Arch}}
    Kernel version:  {{KernelVersion}}
    Experimental:    {{Experimental}}
""", versions)

    def final(self):
        return self.settings[self.name]
