# dokcer - Python based Assistance for Docker

## **Table of contents**

* [Releases](#releases)
* [Status quo](#status)
* [Feature](#feature)
* [Install](#install)
* [Contribute](#contribute)
* [LICENSE](#license)

---------------------------------------

[![asciicast](https://asciinema.org/a/98062.png)](https://asciinema.org/a/98062?autoplay=1)

<a name="releases"></a>
## Releases

- 0.1 -- Initial release
- 0.2 -- More commands supported
- 0.3 -- More commands and options
- 0.4 -- Commands and options are almost done, except for swarm, node, service categories
- 0.5 -- Now it's usable :tada:
- 0.6 -- Fix format problems within lots of commands

<a name="status"></a>
## Status quo

- Currently support following commands:
    - dokcer `version, info, inspect, images, pull, build, run, save, logs, stats, rename, restart, exec, rmi, rm, ps, top, history, cp`
    - dokcer network `ls, create, rm, remove, inspect, connect, disconnect`
    - dokcer volume `ls, create, rm, remove, inspect`

- Plugins feature is testing right now, and each plugin should has its own folder with `__init__.py` inside. Plugins folder struture shows like:

```
$HOME
└───.dokcer
    └───plugins
        ├── plugin_A - __init__.py, ...
        ├── plugin_B - __init__.py, ...
        └───__init__.py
```

- Sample plugin to remove "ALL" containers at once:

```python
"""This module contains `docker rm` class"""

from docker.errors import APIError
from dokcer.lib.Docker.command import Command
from dokcer.cli import Dokcer


class Rm(Command):
    """This class implements `docker rm` command"""

    name = "rm"
    require = []

    def __init__(self):
        Command.__init__(self)
        self.settings[self.name] = None

    def eval_command(self, args):
        try:
            containers = args["containers"]
            del args["containers"]
            Ids = []
            if "ALL" in containers: # dokcer rm ALL
                d = Dokcer()
                d.parse('ps -a --format {{Id}}')
                d.send()
                ress = d.recv()
                if ress:
                    ress = ress.split('\n')
                    ress = [res[0:4] for res in ress]
                    for Id in ress:
                        Ids.append(Id)
                        args['container'] = Id
                        self.client.remove_container(**args)
                        del args['container']
            else:
                for Id in containers:
                    Ids.append(Id)
                    args['container'] = Id
                    self.client.remove_container(**args)
                    del args['container']
            self.settings[self.name] = '\n'.join(Ids)

        except APIError as e:
            raise e

    def final(self):
        return self.settings[self.name]
```

- **If you want auto-complete feature, you could use [bash completion for dokcer](completion/dokcer), taken and modified from docker one, or configure [argcomplete](https://github.com/kislyuk/argcomplete).**

<a name="feature"></a>
## Feature

- You can run any command docker can run on dokcer.
- It's written in Python with love of docker API, so you can tune it by yourself!
- It means you can have your own implementation of docker command line tool. :smirk:

<a name="install"></a>
## Install

### Normal Way

1. `pip install dokcer`, or
2. Clone the repo, and `sudo python ./setup.py install`

### Docker Way

1. Pull from docker hub
    - `docker pull qazbnm456/dokcer`
        - `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock qazbnm456/dokcer version`

2. Build it yourself
    - [Dockerfile](Dockerfile) is provided, and you can build it with: `docker build -t dokcer .`. Once you finished, you'd like to run any command, such as:
        - `docker run --rm -v /var/run/docker.sock:/var/run/docker.sock dokcer version`

![dokcer_version](http://i.imgur.com/t8zcoK9.png "dokcer_version")

<a name="contribute"></a>
## Contribute

| Linux | Windows | MacOSX |
|------------------|---------|---------|
| ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.3-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.3-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker%20version-1.12.3-blue.svg) |

Wanna enrich the possibilities that dokcer can inspire? Send pull requests or issues immediately!

<a name="license"></a>
## LICENSE

This project use [Apache License, Version 2.0](LICENSE).
