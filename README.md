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
## Latest Releases

- 0.9.3 - Add `events` commmand, and fix some option problems
- 0.9.4 - Correct the value of `since` argument of `logs` command

<a name="status"></a>
## Status quo

- Currently support following commands:
    - tsaotun `version, info, events, inspect, images, pull, build, run, save, logs, stats, stop, rename, restart, exec, rmi, rm, ps, top, history, cp`
    - tsaotun container `inspect, run, logs, stats, stop, rename, restart, exec ,rm, ls, top, cp`
    - tsaotun image `inspect, ls, pull, build, save, rm, history`
    - tsaotun network `inspect, ls, create, rm, remove, connect, disconnect`
    - tsaotun volume `inspect, ls, create, rm, remove`
    - tsaotun addon `ls, enable, disable, inspect, install, rm`

- Addon feature is testing right now, and each addon should has its own folder with `__init__.py` inside. Addon folder struture shows like:

```
$HOME
└───Tsaotun
    └───addons
        ├── addon_A - __init__.py, ...
        ├── addon_B - __init__.py, ...
        └───__init__.py
```

- We now have a sample addon called [toolbox](https://github.com/qazbnm456/toolbox), and you can check it out to see how to write an addon on your own.

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
| ![Compatibility Docker Version](https://img.shields.io/badge/docker-17.10.0--ce-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker-17.10.0--ce-blue.svg) | ![Compatibility Docker Version](https://img.shields.io/badge/docker-17.10.0--ce-blue.svg) |

Wanna enrich the possibilities that tsaotun can inspire? Send pull requests or issues immediately!

<a name="license"></a>
## LICENSE

This project use [Apache License, Version 2.0](LICENSE).
