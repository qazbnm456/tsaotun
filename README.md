# dokcer - Python based Assistance for Docker

## **Table of contents**

* [Releases](#releases)
* [Status quo](#status)
* [Feature](#feature)
* [Install](#install)
* [Contribute](#contribute)
* [LICENSE](#license)

---------------------------------------

[![asciicast](https://asciinema.org/a/97089.png)](https://asciinema.org/a/97089?autoplay=1)

<a name="releases"></a>
## Releases

- 0.1 -- Initial release
- 0.2 -- More commands supported
- 0.3 -- More commands and options
- 0.4 -- Commands and options are almost done, except for swarm, node, service categories.
- 0.5 -- Now it's usable. :tada:

<a name="status"></a>
## Status quo

- Currently support following commands:
    - dokcer `version, info, inspect, images, pull, build, run, logs, stats, rename, restart, exec, rmi, rm, ps, top, history, cp`
    - dokcer network `ls, create, rm, remove, inspect, connect, disconnect`
    - dokcer volume `ls, create, rm, remove, inspect`

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
