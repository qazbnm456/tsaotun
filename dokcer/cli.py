# PYTHON_ARGCOMPLETE_OK
# -*- coding: UTF-8 -*-

from __future__ import absolute_import

from sys import exit
import argparse
import textwrap
import argcomplete
from docker.errors import APIError
from requests import ConnectionError

from . import __version__
from .lib.docker_client import Docker
from .lib.Utils import logger


class Dokcer(object):
    """Entrypoint of Dokcer"""
    color = 0
    debug = 0
    dry = 0
    level = 0
    verbose = 0
    remove = False

    def __init__(self, **intruders):
        self.docker = Docker()
        self.push(**intruders)

    def set_color(self):
        """Set terminal color"""
        self.color = 1

    def set_debug(self):
        """DEBUG on/off"""
        self.debug = 1

    def set_dry(self):
        """dry-run on/off"""
        self.dry = 1

    def set_verbose(self, level):
        """Set verbosity level"""
        self.verbose = min(level, 3)

    def push(self, **kwargs):
        """Push custom classes to docker"""
        self.docker.push(**kwargs)

    def eval(self, args, suppress=False):
        """Evaluate commands"""
        try:
            command_flag = args["command_flag"]
            del args["console"]
            del args["color"]
            del args["debug"]
            del args["dry"]
            del args["verbosity"]
            if (command_flag == "run") and ("rm" in args):
                self.remove = args["rm"]
                del args["rm"]
            else:
                self.remove = False
        except KeyError:
            self.docker.load(args)
            return self.docker.recv()  # docker --version

        self.docker.load(args, dry=self.dry)
        if self.remove:
            self.docker.client.remove_container(
                self.docker.recv()["create"]["Id"], force=True)
        if command_flag == "run":
            self.docker.set_recv(self.docker.recv()["run"])
        if suppress is not True:
            if self.color:
                logger.Logger.logSuccess("{}", self.docker.recv())
            else:
                logger.Logger.log("{}", self.docker.recv())


def cli(args=None, **intruders):
    """Entry point of dokcer"""
    try:
        dokcer = Dokcer(**intruders)
        # -------------------------START------------------------------
        p = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter)
        p.add_argument('--console', '-c',
                       action="store_true",
                       help="enter console mode")
        p.add_argument('--color',
                       action="store_true",
                       help="set terminal color")
        p.add_argument('--debug',
                       action="store_true",
                       help="debug on/off")
        p.add_argument('--dry',
                       action="store_true",
                       help="dry-run on/off")
        p.add_argument('--verbose', '-v',
                       action="count", dest="verbosity", default=0,
                       help="set verbosity level")
        p.add_argument('--version',
                       action="version",
                       version="%(prog)s {} with:\n{}\n".format(__version__, dokcer.eval({"command_flag": "version"})))

        # ------------------------------------------------------------

        sp = p.add_subparsers(
            title="Commands", dest="command_flag", help='type [COMMAND] --help to get additional help')

        # --------------------------VERSION--------------------------

        version = sp.add_parser('version',
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                usage="%(prog)s [OPTIONS]",
                                description=textwrap.dedent('''\
        Show the Docker version information
         '''))
        version.add_argument('--format',
                             type=str,
                             help="Pretty-print containers using a Python template")

        # ----------------------------INFO----------------------------

        sp.add_parser('info',
                      formatter_class=argparse.RawDescriptionHelpFormatter,
                      usage="%(prog)s",
                      description=textwrap.dedent('''\
        Display system-wide information
         '''))

        # ---------------------------INSPECT--------------------------

        inspect = sp.add_parser(
            'inspect', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s [OPTIONS] CONTAINER|IMAGE|TASK [CONTAINER|IMAGE|TASK...]",
            description=textwrap.dedent('''\
            Return low-level information on a container, image or task
            '''))
        inspect.add_argument('object',
                             type=str,
                             help="Return low-level information on a container, image or task")
        inspect.add_argument('--format', '-f',
                             type=str,
                             dest="format",
                             help="Pretty-print containers using a Python template")

        # --------------------------IMAGES----------------------------

        images = sp.add_parser('images',
                               formatter_class=argparse.RawDescriptionHelpFormatter,
                               usage="%(prog)s [OPTIONS] [REPOSITORY[:TAG]]",
                               description=textwrap.dedent('''\
        List images
         '''))
        images.add_argument('--all', '-a',
                            action="store_true",
                            dest="all",
                            help="Show all images (default hides intermediate images)")
        images.add_argument('--digests',
                            action="store_true",
                            dest="digests",
                            help="Show digests")
        images.add_argument('--filter', '-f',
                            type=lambda kv: kv.split("=", 1),
                            action="append",
                            dest="filters",
                            help="Filter output based on conditions provided")
        images.add_argument('--format',
                            type=str,
                            help="Pretty-print containers using a Python template")
        images.add_argument('--quiet', '-q',
                            action="store_true",
                            help="Only show numeric IDs")

        # ---------------------------PULL------------------------------

        pull = sp.add_parser('pull',
                             formatter_class=argparse.RawDescriptionHelpFormatter,
                             usage="%(prog)s [OPTIONS] NAME[:TAG|@DIGEST]",
                             description=textwrap.dedent('''\
        Pull an image or a repository from a registry
         '''))
        pull.add_argument('image',
                          type=str,
                          metavar="IMAGE",
                          nargs=1,
                          help="Image to pull")

        # ---------------------------BUILD-----------------------------

        build = sp.add_parser('build',
                              formatter_class=argparse.RawDescriptionHelpFormatter,
                              usage="%(prog)s [OPTIONS] PATH | URL | -",
                              description=textwrap.dedent('''\
        Build an image from a Dockerfile
         '''))
        build.add_argument('path',
                           type=str,
                           metavar="PATH",
                           help="The path containing Dockerfile")
        build.add_argument('--tag', '-t',
                           type=str,
                           dest="tag",
                           help="Name and optionally a tag in the 'name:tag' format")
        build.add_argument('--rm',
                           action="store_true",
                           default=True,
                           help="Remove intermediate containers after a successful build (default true)")

        # ---------------------------RUN------------------------------

        run = sp.add_parser('run',
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            usage="%(prog)s [OPTIONS] IMAGE [COMMAND] [ARG...]",
                            description=textwrap.dedent('''\
        Run a command in a new container
         '''))
        run.add_argument('image',
                         type=str,
                         metavar="IMAGE",
                         help="Image to run")
        run.add_argument('command',
                         type=str,
                         metavar="COMMAND",
                         nargs="*",
                         help="Command to run")
        run.add_argument('--add-host',
                         type=lambda kv: kv.split(":", 1),
                         action="append",
                         dest="extra_hosts",
                         metavar="list",
                         help="Add a custom host-to-IP mapping (host:ip) (default [])")
        run.add_argument('--blkio-weight',
                         type=int,
                         dest="blkio_weight",
                         metavar="uint16",
                         default=0,
                         help="Block IO (relative weight), between 10 and 1000, or 0 to disable (default 0)")
        run.add_argument('--cap-add',
                         action="append",
                         type=str,
                         dest="cap_add",
                         metavar="list",
                         help="Add Linux capabilities (default [])")
        run.add_argument('--cap-drop',
                         action="append",
                         type=str,
                         dest="cap_drop",
                         metavar="list",
                         help="Drop Linux capabilities (default [])")
        run.add_argument('--cgroup-parent',
                         type=str,
                         dest="cgroup_parent",
                         metavar="string",
                         help="Optional parent cgroup for the container")
        run.add_argument('--cidfile',
                         type=str,
                         dest="cidfile",
                         metavar="string",
                         help="Write the container ID to the file")
        run.add_argument('--cpu-period',
                         type=int,
                         dest="cpu_period",
                         metavar="int",
                         help="Limit CPU CFS (Completely Fair Scheduler) period")
        run.add_argument('--cpu-quota',
                         type=int,
                         dest="cpu_quota",
                         metavar="int",
                         help="Limit CPU CFS (Completely Fair Scheduler) quota")
        run.add_argument('--cpu-shares', '-c',
                         type=int,
                         dest="cpu_shares",
                         metavar="int",
                         help="CPU shares (relative weight)")
        run.add_argument('--cpuset-cpus',
                         type=str,
                         dest="cpuset_cpus",
                         metavar="string",
                         help="CPUs in which to allow execution (0-3, 0,1)")
        run.add_argument('--cpuset-mems',
                         type=str,
                         dest="cpuset_mems",
                         metavar="string",
                         help="MEMs in which to allow execution (0-3, 0,1)")
        run.add_argument('--detach', '-d',
                         action="store_true",
                         dest="detach",
                         help="Run container in background and print container ID")
        run.add_argument('--device',
                         action="append",
                         type=str,
                         dest="devices",
                         metavar="list",
                         help="Add a host device to the container (default [])")
        run.add_argument('--dns',
                         action="append",
                         type=str,
                         dest="dns",
                         metavar="list",
                         help="Set custom DNS servers (default [])")
        run.add_argument('--dns-option',
                         action="append",
                         type=str,
                         dest="dns_opt",
                         metavar="list",
                         help="Set DNS options (default [])")
        run.add_argument('--dns-search',
                         action="append",
                         type=str,
                         dest="dns_search",
                         metavar="list",
                         help="Set custom DNS search domains (default [])")
        run.add_argument('--entrypoint',
                         type=str,
                         dest="entrypoint",
                         metavar="string",
                         help="Overwrite the default ENTRYPOINT of the image")
        run.add_argument('--env', '-e',
                         action="append",
                         type=str,
                         dest="environment",
                         metavar="list",
                         help="Set environment variables (default [])")
        run.add_argument('--group-add',
                         action="append",
                         type=str,
                         dest="group_add",
                         metavar="list",
                         help="Add additional groups to join (default [])")
        run.add_argument('--health-cmd',
                         type=str,
                         dest="health_cmd",
                         metavar="string",
                         help="Command to run to check health")
        run.add_argument('--health-interval',
                         type=str,
                         dest="health_interval",
                         metavar="duration",
                         help="Time between running the check (ns|us|ms|s|m|h) (default 0s)")
        run.add_argument('--health-retries',
                         type=int,
                         dest="health_retries",
                         metavar="int",
                         help="Consecutive failures needed to report unhealthy")
        run.add_argument('--health-timeout',
                         type=str,
                         dest="health_timeout",
                         metavar="duration",
                         help="Maximum time to allow one check to run (ns|us|ms|s|m|h) (default 0s)")
        run.add_argument('--hostname',
                         type=str,
                         metavar="string",
                         help="Container host name")
        run.add_argument('--interactive', '-i',
                         action="store_true",
                         dest="stdin_open",
                         default=True,
                         help="Keep STDIN open even if not attached")
        run.add_argument('--ip',
                         type=str,
                         dest="ipv4_address",
                         metavar="string",
                         help="Container IPv4 address (e.g. 172.30.100.104)")
        run.add_argument('--ip6',
                         type=str,
                         dest="ipv6_address",
                         metavar="string",
                         help="Container IPv6 address (e.g. 2001:db8::33)")
        run.add_argument('--ipc',
                         type=str,
                         dest="ipc_mode",
                         metavar="string",
                         help="IPC namespace to use")
        run.add_argument('--isolation',
                         type=str,
                         metavar="string",
                         help="Container isolation technology")
        run.add_argument('--kernel-memory',
                         type=str,
                         dest="kernel_memory",
                         metavar="string",
                         help="Kernel memory limit")
        run.add_argument('--label', '-l',
                         type=lambda kv: kv.split("=", 1),
                         action="append",
                         dest="labels",
                         metavar="list",
                         help="Set meta data on a container (default [])")
        run.add_argument('--link',
                         type=str,
                         action="append",
                         dest="links",
                         metavar="list",
                         help="Add link to another container (default [])")
        run.add_argument('--link-local-ip',
                         type=str,
                         action="append",
                         dest="link_local_ips",
                         metavar="list",
                         help="Container IPv4/IPv6 link-local addresses (default [])")
        run.add_argument('--mac-address',
                         type=str,
                         dest="mac_address",
                         metavar="string",
                         help="Container MAC address (e.g. 92:d0:c6:0a:29:33)")
        run.add_argument('--memory', '-m',
                         type=str,
                         dest="mem_limit",
                         metavar="string",
                         help="Memory limit")
        run.add_argument('--memory-reservation',
                         type=str,
                         dest="mem_reservation",
                         metavar="string",
                         help="Memory soft limit")
        run.add_argument('--memory-swap',
                         type=str,
                         dest="memswap_limit",
                         metavar="string",
                         help="Swap limit equal to memory plus swap: '-1' to enable unlimited swap")
        run.add_argument('--memory-swappiness',
                         type=int,
                         dest="mem_swappiness",
                         default=-1,
                         metavar="int",
                         help="Tune container memory swappiness (0 to 100) (default -1)")
        run.add_argument('--name',
                         type=str,
                         metavar="string",
                         help="Assign a name to the container")
        run.add_argument('--network',
                         type=str,
                         dest="network",
                         default="default",
                         metavar="string",
                         help="Connect a container to a network (default \"default\")")
        run.add_argument('--network-alias',
                         type=str,
                         action="append",
                         dest="aliases",
                         metavar="list",
                         help="Add network-scoped alias for the container (default [])")
        run.add_argument('--no-healthcheck',
                         action="store_true",
                         dest="no_healthcheck",
                         help="Disable any container-specified HEALTHCHECK")
        run.add_argument('--oom-kill-disable',
                         action="store_true",
                         dest="oom_kill_disable",
                         help="Disable OOM Killer")
        run.add_argument('--oom-score-adj',
                         type=int,
                         dest="oom_score_adj",
                         metavar="int",
                         help="Tune host's OOM preferences (-1000 to 1000)")
        run.add_argument('--pid',
                         type=str,
                         dest="pid_mode",
                         metavar="string",
                         help="PID namespace to use")
        run.add_argument('--pids-limit',
                         type=int,
                         dest="pids_limit",
                         metavar="int",
                         help="Tune container pids limit (set -1 for unlimited)")
        run.add_argument('--privileged',
                         action="store_true",
                         help="Give extended privileges to this container")
        run.add_argument('--publish', '-p',
                         action="append",
                         type=str,
                         metavar="list",
                         dest="port_bindings",
                         help="Publish a container's port(s) to the host (default [])")
        run.add_argument('--publish-all', '-P',
                         action="store_true",
                         dest="publish_all_ports",
                         help="Publish all exposed ports to random ports")
        run.add_argument('--read-only',
                         action="store_true",
                         dest="read_only",
                         help="Mount the container's root filesystem as read only")
        run.add_argument('--restart',
                         dest="restart_policy",
                         default="no",
                         metavar="string",
                         help="Restart policy to apply when a container exits (default \"no\")")
        run.add_argument('--rm',
                         action="store_true",
                         help="Automatically remove the container when it exits")
        run.add_argument('--security-opt',
                         action="append",
                         dest="security_opt",
                         metavar="list",
                         help="Security Options (default [])")
        run.add_argument('--shm-size',
                         dest="shm_size",
                         default="64MB",
                         metavar="string",
                         help="Size of /dev/shm, default value is 64MB")
        run.add_argument('--stop-signal',
                         type=str,
                         dest="stop_signal",
                         default="SIGTERM",
                         metavar="string",
                         help="Signal to stop a container, SIGTERM by default (default \"SIGTERM\")")
        run.add_argument('--sysctl',
                         type=lambda kv: kv.split("=", 1),
                         action="append",
                         dest="sysctls",
                         metavar="map",
                         help="Sysctl options (default map[])")
        run.add_argument('--tmpfs',
                         type=lambda kv: kv.split(":", 1),
                         action="append",
                         metavar="list",
                         help="Mount a tmpfs directory (default [])")
        run.add_argument('--tty', '-t',
                         action="store_true",
                         dest="tty",
                         help="Allocate a pseudo-TTY")
        run.add_argument('--ulimit',
                         type=lambda kv: kv.split("=", 1),
                         action="append",
                         dest="ulimits",
                         metavar="ulimit",
                         help="Ulimit options (default [])")
        run.add_argument('--userns',
                         type=str,
                         dest="userns_mode",
                         metavar="string",
                         help="User namespace to use")
        run.add_argument('--volume', '-v',
                         action="append",
                         type=str,
                         dest="binds",
                         help=textwrap.dedent('''\
        Bind mount a volume (default []). The format
        is [host-src:]container-dest[:<options>].
        The comma-delimited options are [rw|ro],
        [z|Z], [[r]shared|[r]slave|[r]private], and
        [nocopy]. The 'host-src' is an absolute path
        or a name value.
        '''))
        run.add_argument('--volumes-driver',
                         type=str,
                         dest="volume_driver",
                         metavar="string",
                         help="Optional volume driver for the container")
        run.add_argument('--volumes-from',
                         type=lambda kv: kv.split(":", 1),
                         action="append",
                         dest="volumes_from",
                         metavar="list",
                         help="Mount volumes from the specified container(s) (default [])")

        # --------------------------LOGS------------------------------

        logs = sp.add_parser('logs',
                             formatter_class=argparse.RawDescriptionHelpFormatter,
                             usage="%(prog)s [OPTIONS] CONTAINER",
                             description=textwrap.dedent('''\
        Fetch the logs of a container
         '''))
        logs.add_argument('container',
                          type=str,
                          metavar="CONTAINER",
                          help="Fetch the logs of a container")

        # --------------------------STATS-----------------------------

        stats = sp.add_parser('stats',
                              formatter_class=argparse.RawDescriptionHelpFormatter,
                              usage="%(prog)s [OPTIONS] [CONTAINER...]",
                              description=textwrap.dedent('''\
        Display a live stream of container(s) resource usage statistics
         '''))
        stats.add_argument('containers',
                           type=str,
                           metavar="CONTAINER",
                           nargs="+",
                           help="Display a live stream of container(s) resource usage statistics")
        """
        stats.add_argument('--all', '-a',
                           action="store_true",
                           default=False,
                           help="Show all containers (default shows just running)")
        """
        stats.add_argument('--no-stream',
                           action="store_true",
                           dest="stream",
                           default=True,
                           help="Disable streaming stats and only pull the first result")

        # -------------------------RENAME-----------------------------

        rename = sp.add_parser('rename',
                               formatter_class=argparse.RawDescriptionHelpFormatter,
                               usage="%(prog)s CONTAINER NEW_NAME",
                               description=textwrap.dedent('''\
        Rename a container
         '''))
        rename.add_argument('container',
                            type=str,
                            metavar="CONTAINER",
                            help="Container to be renamed")
        rename.add_argument('name',
                            type=str,
                            metavar="NAME",
                            help="New container name")

        # -------------------------RESTART----------------------------

        restart = sp.add_parser('restart',
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                usage="%(prog)s [OPTIONS] CONTAINER [CONTAINER...]",
                                description=textwrap.dedent('''\
        Restart one or more containers
         '''))
        restart.add_argument('containers',
                             type=str,
                             metavar="CONTAINER",
                             nargs="+",
                             help="Containers to be restarted")
        restart.add_argument('--time', '-t',
                             type=int,
                             metavar='int',
                             dest="timeout",
                             default=10,
                             help="Seconds to wait for stop before killing the container (default 10)")

        # --------------------------EXEC------------------------------

        exec_d = sp.add_parser('exec',
                               formatter_class=argparse.RawDescriptionHelpFormatter,
                               usage="%(prog)s [OPTIONS] CONTAINER COMMAND [ARG...]",
                               description=textwrap.dedent('''\
        Run a command in a running container
         '''))
        exec_d.add_argument('container',
                            type=str,
                            metavar="CONTAINER",
                            help="Target container where exec instance will be created")
        exec_d.add_argument('cmd',
                            type=str,
                            metavar="COMMAND",
                            nargs="+",
                            help="Command to be executed")
        exec_d.add_argument('--detach', '-d',
                            action="store_true",
                            dest="detach",
                            help="Detached mode: run command in the background")
        exec_d.add_argument('--interactive', '-i',
                            action="store_true",
                            dest="stdin_open",
                            default=True,
                            help="Keep STDIN open even if not attached")
        exec_d.add_argument('--tty', '-t',
                            action="store_true",
                            dest="tty",
                            help="Allocate a pseudo-TTY")

        # ---------------------------RMI------------------------------

        rmi = sp.add_parser('rmi',
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            usage="%(prog)s [OPTIONS] IMAGE [IMAGE...]",
                            description=textwrap.dedent('''\
        Remove one or more images
         '''))
        rmi.add_argument('images',
                         type=str,
                         metavar="IMAGE",
                         nargs="+",
                         help="Images to be removed")
        rmi.add_argument('--force', '-f',
                         action="store_true",
                         dest="force",
                         help="Force removal of the image")

        # ---------------------------RM-------------------------------

        rm = sp.add_parser('rm',
                           formatter_class=argparse.RawDescriptionHelpFormatter,
                           usage="%(prog)s [OPTIONS] CONTAINER [CONTAINER...]",
                           description=textwrap.dedent('''\
        Remove one or more containers
         '''))
        rm.add_argument('containers',
                        type=str,
                        metavar="CONTAINER",
                        nargs="+",
                        help="Containers to be removed")
        rm.add_argument('--force', '-f',
                        action="store_true",
                        dest="force",
                        help="Force the removal of a running container (uses SIGKILL)")

        # ---------------------------PS-------------------------------

        ps = sp.add_parser('ps',
                           formatter_class=argparse.RawDescriptionHelpFormatter,
                           usage="%(prog)s [OPTIONS]",
                           description=textwrap.dedent('''\
        List containers
         '''))
        ps.add_argument('--all', '-a',
                        action="store_true",
                        dest="all",
                        help="Show all containers (default shows just running)")
        ps.add_argument('--filter', '-f',
                        type=dict,
                        dest="filters",
                        metavar="filter",
                        help="Filter output based on conditions provided (default [])")
        ps.add_argument('--format',
                        type=str,
                        metavar="string",
                        help="Pretty-print containers using a Python template")
        ps.add_argument('--quiet', '-q',
                        action="store_true",
                        help="Only display numeric IDs")

        # -------------------------TOP--------------------------------

        top = sp.add_parser('top',
                            formatter_class=argparse.RawDescriptionHelpFormatter,
                            usage="%(prog)s CONTAINER [ps OPTIONS]",
                            description=textwrap.dedent('''\
        Display the running processes of a container
         '''))
        top.add_argument('container',
                         type=str,
                         metavar="CONTAINER",
                         help="Display the running processes of a container")
        top.add_argument('ps_args',
                         type=str,
                         nargs="?",
                         help="Ps options")

        # ------------------------HISTORY-----------------------------

        history = sp.add_parser('history',
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                usage="%(prog)s [OPTIONS] IMAGE",
                                description=textwrap.dedent('''\
        Show the history of an image
         '''))
        history.add_argument('image',
                             type=str,
                             metavar="IMAGE",
                             help="Image to show history")

        # --------------------------CP--------------------------------

        cp = sp.add_parser('cp',
                           formatter_class=argparse.RawDescriptionHelpFormatter,
                           usage="%(prog)s [OPTIONS] CONTAINER:SRC_PATH DEST_PATH|-\ndocker cp [OPTIONS] SRC_PATH|- CONTAINER:DEST_PATH",
                           description=textwrap.dedent('''\
        Copy files/folders between a container and the local filesystem

        Use '-' as the source to read a tar archive from stdin
        and extract it to a directory destination in a container.
        Use '-' as the destination to stream a tar archive of a
        container source to stdout.
         '''))
        cp.add_argument('src',
                        type=str,
                        metavar="CONTAINER:SRC_PATH")
        cp.add_argument('dest',
                        type=str,
                        metavar="DEST_PATH")

        # ------------------------NETWORK-----------------------------

        network_p = sp.add_parser('network')
        network = network_p.add_subparsers(
            title="Networks", dest="network_flag", help='type [COMMAND] --help to get additional help')

        # -----------------------NETWORK-LS---------------------------

        network_ls = network.add_parser('ls',
                                        formatter_class=argparse.RawDescriptionHelpFormatter,
                                        usage="%(prog)s [OPTIONS]",
                                        description=textwrap.dedent('''\
        List networks
         '''))
        network_ls.add_argument('--filter', '-f',
                                type=lambda kv: kv.split("=", 1),
                                action="append",
                                dest="filters",
                                metavar="filter",
                                help="Provide filter values (e.g. 'driver=bridge')")
        network_ls.add_argument('--format',
                                type=str,
                                help="Pretty-print networks using a Python template")

        # ---------------------NETWORK-CREATE--------------------------

        network_create = network.add_parser('create',
                                            formatter_class=argparse.RawDescriptionHelpFormatter,
                                            usage="%(prog)s [OPTIONS] NETWORK",
                                            description=textwrap.dedent('''\
        Create a network
         '''))
        network_create.add_argument('name',
                                    type=str,
                                    metavar="NETWORK",
                                    help="Network name")
        network_create.add_argument('--driver', '-d',
                                    type=str,
                                    dest="driver",
                                    default="bridge",
                                    metavar="string",
                                    help="Driver to manage the Network (default \"bridge\")")
        network_create.add_argument('--gateway',
                                    type=str,
                                    dest="gateway",
                                    help="Custom IP address for the pool's gateway.")
        network_create.add_argument('--internal',
                                    action="store_true",
                                    default=False,
                                    help="Restrict external access to the network")
        network_create.add_argument('--ip-range',
                                    type=str,
                                    dest="iprange",
                                    help="Allocate container ip from a sub-range")
        network_create.add_argument('--ipam-driver',
                                    type=str,
                                    dest="ipamdriver",
                                    default="default",
                                    help="IP Address Management Driver (default \"default\")")
        network_create.add_argument('--ipam-opt',
                                    type=lambda kv: kv.split("=", 1),
                                    action="append",
                                    dest="ipamopt",
                                    help="Set IPAM driver specific options (default None)")
        network_create.add_argument('--ipv6',
                                    action="store_true",
                                    dest="enable_ipv6",
                                    default=False,
                                    help="Enable IPv6 networking")
        network_create.add_argument('--label',
                                    type=lambda kv: kv.split("=", 1),
                                    action="append",
                                    dest="labels",
                                    help="Set metadata on a network (default [])")
        network_create.add_argument('--opt', '-o',
                                    type=lambda kv: kv.split("=", 1),
                                    action="append",
                                    dest="options",
                                    help="Set driver specific options")
        network_create.add_argument('--subnet',
                                    type=str,
                                    dest="subnet",
                                    help="Custom subnet for this IPAM pool using the CIDR notation. Defaults to None.")

        # -----------------------NETWORK-RM----------------------------

        network_rm = network.add_parser(
            'rm', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s NETWORK [NETWORK...]",
            description=textwrap.dedent('''\
        Remove one or more networks

        Aliases:
            rm, remove
        '''))
        network_rm.add_argument('networks',
                                type=str,
                                metavar="NETWORK",
                                nargs="+",
                                help="Networks to be removed")

        network_remove = network.add_parser(
            'remove', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s NETWORK [NETWORK...]",
            description=textwrap.dedent('''\
            Remove one or more networks

            Aliases:
              rm, remove
            '''))

        network_remove.add_argument('networks',
                                    type=str,
                                    metavar="NETWORK",
                                    nargs="+",
                                    help="Remove one or more networks")

        # -----------------------NETWORK-INSPECT-----------------------

        network_inspect = network.add_parser(
            'inspect', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s [OPTIONS] NETWORK [NETWORK...]",
            description=textwrap.dedent('''\
            Display detailed information on one or more networks
            '''))
        network_inspect.add_argument('networks',
                                     type=str,
                                     metavar="NETWORK",
                                     nargs="+",
                                     help="Display detailed information on one or more networks")
        network_inspect.add_argument('--format', '-f',
                                     type=str,
                                     dest="format",
                                     help="Pretty-print containers using a Python template")

        # ------------------------NETWORK-CONNECT-----------------------

        network_connect = network.add_parser(
            'connect', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s [OPTIONS] NETWORK CONTAINER",
            description=textwrap.dedent('''\
            Connect a container to a network
            '''))
        network_connect.add_argument('net_id',
                                     type=str,
                                     metavar="NETWORK",
                                     help="Network to be connected")
        network_connect.add_argument('container',
                                     type=str,
                                     metavar="CONTAINER",
                                     help="Container to be assigned")
        network_connect.add_argument('--alias',
                                     action="append",
                                     type=str,
                                     dest="aliases",
                                     metavar="stringSlice",
                                     help="Add network-scoped alias for the container")
        network_connect.add_argument('--ip',
                                     type=str,
                                     dest="ipv4_address",
                                     metavar="string",
                                     help="IP Address")
        network_connect.add_argument('--ip6',
                                     type=str,
                                     dest="ipv6_address",
                                     metavar="string",
                                     help="IPv6 Address")
        network_connect.add_argument('--link',
                                     action="append",
                                     type=str,
                                     dest="links",
                                     metavar="list",
                                     help="Add link to another container (default [])")
        network_connect.add_argument('--link-local-ip',
                                     action="append",
                                     type=str,
                                     dest="link_local_ips",
                                     metavar="stringSlice",
                                     help="Add a link-local address for the container")

        # ------------------------NETWORK-DISCONNECT--------------------

        network_disconnect = network.add_parser(
            'disconnect', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s [OPTIONS] NETWORK CONTAINER",
            description=textwrap.dedent('''\
            Disconnect a container from a network
            '''))
        network_disconnect.add_argument('net_id',
                                        type=str,
                                        metavar="NETWORK",
                                        help="Network to be disconnected")
        network_disconnect.add_argument('container',
                                        type=str,
                                        metavar="CONTAINER",
                                        help="Container to be assigned")
        network_disconnect.add_argument('--force', '-f',
                                        action="store_true",
                                        dest="force",
                                        help="Force the container to disconnect from a network")

        # ---------------------------NETWORK-PRUNE----------------------

        """
        network_prune = network.add_parser(
            'prune', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s [OPTIONS]",
            description=textwrap.dedent('''\
            Remove all unused networks
            '''))
        network_prune.add_argument('--force', '-f',
                                   action="store_true",
                                   dest="force",
                                   help="Do not prompt for confirmation")
        """

        # -------------------------VOLUME-----------------------------

        volume_p = sp.add_parser('volume')
        volume = volume_p.add_subparsers(
            title="Volumes", dest="volume_flag", help='type [COMMAND] --help to get additional help')

        # ------------------------VOLUME-LS---------------------------

        volume_ls = volume.add_parser('ls',
                                      formatter_class=argparse.RawDescriptionHelpFormatter,
                                      usage="%(prog)s [OPTIONS]",
                                      description=textwrap.dedent('''\
        List volumes
         '''))
        volume_ls.add_argument('--filter', '-f',
                               type=lambda kv: kv.split("=", 1),
                               action="append",
                               dest="filters",
                               metavar="filter",
                               help="Provide filter values (e.g. 'dangling=true')")
        volume_ls.add_argument('--format',
                               type=str,
                               help="Pretty-print networks using a Python template")

        # ----------------------VOLUME-CREATE--------------------------

        volume_create = volume.add_parser('create',
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          usage="%(prog)s [OPTIONS] [VOLUME]",
                                          description=textwrap.dedent('''\
        Create a volume
         '''))
        volume_create.add_argument('name',
                                   type=str,
                                   metavar="VOLUME",
                                   help="Volume name")
        volume_create.add_argument('--driver', '-d',
                                   type=str,
                                   dest="driver",
                                   default="local",
                                   metavar="string",
                                   help="Specify volume driver name (default \"local\")")
        volume_create.add_argument('--opt', '-o',
                                   type=lambda kv: kv.split("=", 1),
                                   action="append",
                                   dest="driver_opts",
                                   metavar="map",
                                   help="Set driver specific options (default map[])")
        volume_create.add_argument('--label',
                                   type=lambda kv: kv.split("=", 1),
                                   action="append",
                                   dest="labels",
                                   metavar="list",
                                   help="Set metadata for a volume (default [])")

        # ------------------------VOLUME-RM----------------------------

        volume_rm = volume.add_parser('rm',
                                      formatter_class=argparse.RawDescriptionHelpFormatter,
                                      usage="%(prog)s [OPTIONS] VOLUME [VOLUME...]",
                                      description=textwrap.dedent('''\
        Remove one or more volumes

        Aliases:
        rm, remove

        Examples:

        $ docker volume rm hello
        hello
         '''))
        volume_rm.add_argument('volumes',
                               type=str,
                               metavar="VOLUME",
                               nargs="+",
                               help="Volumes to be removed")

        volume_remove = volume.add_parser('remove',
                                          formatter_class=argparse.RawDescriptionHelpFormatter,
                                          usage="%(prog)s [OPTIONS] VOLUME [VOLUME...]",
                                          description=textwrap.dedent('''\
        Remove one or more volumes

        Aliases:
        rm, remove

        Examples:

        $ docker volume rm hello
        hello
         '''))
        volume_remove.add_argument('volumes',
                                   type=str,
                                   metavar="VOLUME",
                                   nargs="+",
                                   help="Volumes to be removed")

        # ------------------------VOLUME-INSPECT-----------------------

        volume_inspect = volume.add_parser(
            'inspect', formatter_class=argparse.RawDescriptionHelpFormatter,
            usage="%(prog)s [OPTIONS] VOLUME [VOLUME...]",
            description=textwrap.dedent('''\
            Display detailed information on one or more volumes
            '''))
        volume_inspect.add_argument('volumes',
                                    type=str,
                                    metavar="VOLUME",
                                    nargs="+",
                                    help="Display detailed information on one or more volumes")
        volume_inspect.add_argument('--format', '-f',
                                    type=str,
                                    dest="format",
                                    help="Pretty-print containers using a Python template")

        # ---------------------------END------------------------------

        argcomplete.autocomplete(p)
        if args:
            arguments = p.parse_args(args.split())
        else:
            arguments = p.parse_args()
        arguments = vars(arguments)

        if arguments["console"]:
            enter_shell(dokcer)
        else:
            dokcer.set_verbose(arguments["verbosity"])
            if arguments["color"]:
                dokcer.set_color()
            if arguments["debug"]:
                dokcer.set_debug()
            if arguments["dry"]:
                dokcer.set_dry()

        dokcer.eval(arguments)

        if dokcer.debug:
            import json
            print json.dumps(
                arguments, indent=4)
    except (KeyboardInterrupt, SystemExit):
        pass
    except ConnectionError as e:
        logger.Logger.log("Error response from dokcer: {}\n", e.message[0])
        exit(1)
    except (AttributeError, ValueError) as e:
        if dokcer.color:
            logger.Logger.logError("Error response from dokcer: {}", str(e))
        else:
            logger.Logger.log("Error response from dokcer: {}", str(e))
        exit(1)
    except APIError as e:
        try:
            msg = e.response.json()["message"]
        except ValueError:
            msg = str(e.response.text[:-1])
        logger.Logger.log("Error response from daemon: {}", msg)
        exit(1)
