# Tsaotun - Python based Assistance for Docker

## **Table of contents**

* [Releases](#releases)
* [Status quo](#status)
* [Feature](#feature)
* [Install](#install)
* [Contribute](#contribute)
* [LICENSE](#license)

---------------------------------------

[![asciicast](https://asciinema.org/a/99422.png)](https://asciinema.org/a/99422?autoplay=1)

<a name="releases"></a>
## Releases

- 0.5 -- First usable version :tada:
- 0.6 -- Fix format problems within lots of commands
- 0.7 -- Code cleanup and move root commands into their command groups (such as container, image, network, and etc)
- 0.8 -- Addon feature works, but is still under heavy development.
- 0.8.1 -- Change name from 'Dokcer' to 'Tsaotun'.
- 0.8.2 -- Addon feature is close to stable.
- 0.8.3 -- Nevermind, just a typo fixed.

<a name="status"></a>
## Status quo

- Currently support following commands:
    - tsaotun `version, info, inspect, images, pull, build, run, save, logs, stats, rename, restart, exec, rmi, rm, ps, top, history, cp`
    - tsaotun container `inspect, run, logs, stats, rename, restart, exec ,rm, ls, top, cp`
    - tsaotun image `inspect, ls, pull, build, save, rm, history`
    - tsaotun network `inspect, ls, create, rm, remove, connect, disconnect`
    - tsaotun volume `inspect, ls, create, rm, remove`
    - tsaotun addon `ls, enable, disable, inspect`

- Addon feature is testing right now, and each addon should has its own folder with `__init__.py` inside. Addon folder struture shows like:

```
$HOME
└───Tsaotun
    └───addons
        ├── addon_A - __init__.py, ...
        ├── addon_B - __init__.py, ...
        └───__init__.py
```

- Sample addon to remove "ALL" containers at once, no matter it's dead or alive:
    - ### __init__.py: To specify how to override the original command
        ```python
        """Configuration file for this addon"""

        from .Container import rm

        __override__ = {'Container.rm': 'Rm'}
        __argparse__ = [
            {
                'namespace': "Container",
                'position': "Child",
                'subcommand': "rm",
                'actions': [
                    "add_argument('--clear',            \
                                   action='store_true', \
                                   dest='clear',        \
                                   help='Remove all dead and alive containers. \
                                         You still need to give a whatever container ID.')",
                ],
            },
        ]
        ```

    - ### Container/rm.py
        ```python
        """This module contains `docker container rm` class"""

        from docker.errors import APIError
        from tsaotun.lib.Docker.Container.command import Command
        from tsaotun.cli import Tsaotun


        class Rm(Command):
            """This class implements `docker container rm` command"""

            name = "container rm"
            require = []

            def __init__(self):
                Command.__init__(self)
                self.settings[self.name] = None

            def eval_command(self, args):
                try:
                    containers = args["containers"]
                    clear = args["clear"]
                    del args["containers"]
                    del args["clear"]
                    Ids = []
                    if clear:
                        cli = Tsaotun()
                        cli.send('ps -a --format {{Id}}')
                        ress = cli.recv()
                        if ress:
                            ress = ress.split('\n')
                            ress = [res[0:4] for res in ress]
                            for Id in ress:
                                Ids.append(Id)
                                args['container'] = Id
                                self.client.remove_container(**args)
                    else:
                        for Id in containers:
                            Ids.append(Id)
                            args['container'] = Id
                            self.client.remove_container(**args)
                    self.settings[self.name] = '\n'.join(Ids)

                except APIError as e:
                    raise e

            def final(self):
                return self.settings[self.name]
        ```

- **If you want auto-complete feature, you could use [bash completion for tsaotun](completion/tsaotun), taken and modified from docker one, or configure [argcomplete](https://github.com/kislyuk/argcomplete).**

<a name="feature"></a>
## Feature

- You can run any command docker can run on Tsaotun.
- It's written in Python with love of API of docker, so you can tune it by yourself!
- It means you can have your own implementation of docker command line tool. :smirk:

<a name="install"></a>
## Install

### Normal Way

1. `pip install tsaotun`, or
2. Clone the repo, and `python ./setup.py install`

### Docker Way

1. Pull from docker hub
    - `docker pull qazbnm456/tsaotun`
        - `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock qazbnm456/tsaotun version`

2. Build it yourself
    - [Dockerfile](Dockerfile) is provided, and you can build it with: `docker build -t tsaotun .`. Once you finished, you'd like to run any command, such as:
        - `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock tsaotun version`

<img src="http://i.imgur.com/WRkfRoq.png" width="540">

<a name="contribute"></a>
## Contribute

| Linux | Windows | MacOSX |
|------------------|---------|---------|
| ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.13.0-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.13.0-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.13.0-blue.svg) |

Wanna enrich the possibilities that tsaotun can inspire? Send pull requests or issues immediately!

<a name="license"></a>
## LICENSE

This project use [Apache License, Version 2.0](LICENSE).
