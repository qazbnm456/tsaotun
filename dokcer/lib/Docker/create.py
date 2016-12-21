"""This module contains `docker create` class"""

import time
from hashlib import sha1
from docker.errors import APIError

from .command import Command

SECOND = 1000000000


class Create(Command):
    """This class implements `docker create` command"""

    name = "create"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def preprocess(self, args):
        """Preprocess arguments provided for `docker create`"""
        # port_bindings
        ports = []
        if args.get("port_bindings"):
            port_bindings = args["port_bindings"]
            args["port_bindings"] = {}
            for port_binding in port_bindings:
                host, container = port_binding.strip('{}').split(':', 2)
                args["port_bindings"].update([[container, host], ])
                ports.append(container)

        # binds
        volumes = []
        if args.get("binds"):
            volume_bindings = args["binds"]
            args["binds"] = []
            for volume_binding in volume_bindings:
                try:
                    host, container, _ = volume_binding.split(':', 3)
                except ValueError:
                    host, container = volume_binding.split(':', 2)
                args["binds"].append(volume_binding)
                volumes.append(container)

        # image
        image = args["image"]
        del args["image"]

        # command
        if "command" in args:
            command = args["command"]
            del args["command"]

        # hostname
        if "hostname" in args:
            hostname = args["hostname"]
            del args["hostname"]

        # cidfile
        if args.get("cidfile"):
            cidfile = args["cidfile"]
        else:
            cidfile = None
        del args["cidfile"]

        # detach
        detach = args["detach"]
        del args["detach"]

        # entrypoint
        entrypoint = args["entrypoint"]
        del args["entrypoint"]

        # environment
        environment = args["environment"]
        del args["environment"]

        # healthcheck
        have_health_settings = bool(args["health_cmd"]) | bool(args["health_interval"]) | bool(
            args["health_timeout"]) | bool(args["health_retries"])
        if args["no_healthcheck"]:
            healthcheck = None
        elif have_health_settings:
            from ..Utils.duration_conversion import from_str
            healthcheck = dict(
                test=args["health_cmd"] if args["health_cmd"] else None,
                interval=from_str(
                    args["health_interval"]).seconds * SECOND if args["health_interval"] else None,
                timeout=from_str(args["health_timeout"]).seconds *
                SECOND if args["health_timeout"] else None,
                retries=args["health_retries"] if args[
                    "health_retries"] else None,
            )
        else:
            healthcheck = None
        del args["health_cmd"]
        del args["health_interval"]
        del args["health_timeout"]
        del args["health_retries"]
        del args["no_healthcheck"]

        # labels
        labels = dict(args["labels"]) if args["labels"] else None
        del args["labels"]

        # mac_address
        mac_address = args["mac_address"]
        del args["mac_address"]

        # name
        name = args["name"]
        del args["name"]

        # stop_signal
        stop_signal = args["stop_signal"]
        del args["stop_signal"]

        # tty
        tty = args["tty"]
        del args["tty"]

        # volume_driver
        volume_driver = args["volume_driver"]
        del args["volume_driver"]

        # stdin_open
        stdin_open = args["stdin_open"]
        del args["stdin_open"]

        # create_networking_config
        network = args["network"]
        ipv4_address = args["ipv4_address"]
        ipv6_address = args["ipv6_address"]
        aliases = args["aliases"]
        links = args["links"]
        link_local_ips = args["link_local_ips"]
        del args["network"]
        del args["ipv4_address"]
        del args["ipv6_address"]
        del args["aliases"]
        del args["links"]
        del args["link_local_ips"]
        networking_config = self.client.create_networking_config({
            '{}'.format(network): self.client.create_endpoint_config(
                ipv4_address=ipv4_address,
                ipv6_address=ipv6_address,
                aliases=aliases,
                links=links,
                link_local_ips=link_local_ips
            )
        })

        # host_config
        # wait for PR: https://github.com/docker/docker-py/pull/1363
        del args["cpuset_mems"]
        args["extra_hosts"] = dict(args["extra_hosts"]) if args[
            "extra_hosts"] else None
        args["restart_policy"] = {
            "Name": args["restart_policy"],
            "MaximumRetryCount": 0
        }
        args["sysctls"] = dict(args["sysctls"]) if args["sysctls"] else None
        args["tmpfs"] = dict(args["tmpfs"]) if args["tmpfs"] else None
        args["ulimits"] = dict(args["ulimits"]) if args["ulimits"] else None
        args["volumes_from"] = dict(args["volumes_from"]) if args[
            "volumes_from"] else None
        host_config = self.client.create_host_config(**args)
        del args["extra_hosts"]
        del args["blkio_weight"]
        del args["cap_add"]
        del args["cap_drop"]
        del args["cgroup_parent"]
        del args["cpu_period"]
        del args["cpu_quota"]
        del args["cpu_shares"]
        del args["cpuset_cpus"]
        # del args["cpuset_mems"]
        del args["devices"]
        del args["dns"]
        del args["dns_opt"]
        del args["dns_search"]
        del args["group_add"]
        del args["ipc_mode"]
        del args["isolation"]
        del args["kernel_memory"]
        del args["mem_limit"]
        del args["mem_reservation"]
        del args["memswap_limit"]
        del args["mem_swappiness"]
        del args["oom_kill_disable"]
        del args["oom_score_adj"]
        del args["pid_mode"]
        del args["pids_limit"]
        del args["privileged"]
        del args["publish_all_ports"]
        del args["read_only"]
        del args["restart_policy"]
        del args["security_opt"]
        del args["shm_size"]
        del args["sysctls"]
        del args["tmpfs"]
        del args["ulimits"]
        del args["userns_mode"]

        # store back arguments
        del args["port_bindings"]
        args["ports"] = ports
        del args["binds"]
        args["volumes"] = volumes
        args["networking_config"] = networking_config
        args["command"] = command
        args["host_config"] = host_config
        args["image"] = image
        args["hostname"] = hostname
        args["cidfile"] = cidfile
        args["name"] = name
        args["detach"] = detach
        args["entrypoint"] = entrypoint
        args["environment"] = environment
        args["healthcheck"] = healthcheck
        args["labels"] = labels
        args["mac_address"] = mac_address
        args["name"] = name
        args["stop_signal"] = stop_signal
        args["tty"] = tty
        args["volume_driver"] = volume_driver
        args["stdin_open"] = stdin_open

    def eval_command(self, args):
        """Create host config for containers"""
        try:
            self.preprocess(args)
            # cidfile
            if args["cidfile"]:
                cidfile = args["cidfile"]
            else:
                cidfile = None
            del args["cidfile"]
            self.settings[self.name] = self.client.create_container(**args)
            if cidfile:
                with open(cidfile, 'w') as fd:
                    fd.write(self.settings[self.name]["Id"])
        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
