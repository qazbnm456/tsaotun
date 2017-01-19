Tsaotun - Python based Assistance for Docker
############################################

**Q: I can't figure out why I would need this**

A: 

In traditional ways, we make aliases ourselves all over the Docker commands.

The reason why I develop this project is to encourage people to contribute and share their ideas and thoughts into plugins, which would give Tsaotun ability to do those things. And, the aboved thing is just one of things that Tsaotun can achieve, you will be able to load variety of plugins in the future as well.

Besides, if you are doing some projects involved running containers, Tsaotun has provide the higher level API for you. That is another helpful functionality.

Currently, I'm moving my previous project `VWGen`_ into one of Tsaotun's plugin. Once I finish, everyone can just load the plugin and extend the power of Tsaotun.


.. class:: no-web

    .. image:: http://i.imgur.com/WRkfRoq.png
        :alt: Higher level API
        :width: 100%
        :align: center


.. class:: no-web no-pdf

|pypi| |unix_docker| |mac_docker| |windows_docker|



.. contents::

.. section-numbering::


Main features
=============

* Run any commands docker can run on Tsaotun
* All written in Python with love of API of docker
* Simplify the process making your own implementation of docker command line tool
* Many Addons are upcoming


Installation (All platforms)
============================


pip
---


A universal installation method (that works on Windows, Mac OS X, Linux, and always provides the latest version) is to use `pip`_:


.. code-block:: bash

    # Make sure we have an up-to-date version of pip and setuptools:
    $ pip install --upgrade pip setuptools

    $ pip install --upgrade tsaotun


(If ``pip`` installation fails for some reason, you can try
``easy_install tsaotun`` as a fallback.)


Docker hub
----------

Pull from `dockerhub`_, or build it yourself:


.. code-block:: bash

    $ docker build -t tsaotun .


Verify that now we have installed the latest version, for example:


.. code-block:: bash

    $ tsaotun version
    Client:
        Version:         0.8.1
        Python version:  2.7.13
        OS/Arch:         Darwin/x86_64

    Server:
        Version:         1.13.0-rc7
        API version:     1.25 (minimum version 1.12)
        Go version:      go1.7.3
        Git commit:      48a9e53
        Built:           5 days ago
        OS/Arch:         linux/amd64
        Kernel version:  4.9.3-moby
        Experimental:    True


Usage
=====


Hello World:


.. code-block:: bash

    $ tsaotun [COMMAND]


Synopsis:

.. code-block:: bash

    $ tsaotun [-h] [--console] [--color] [--debug] [--dry] [--host list]
              [--verbose]
              {version,info,inspect,container,image,network,volume,addon}
              ...


See also ``tsaotun --help``.


Addon
=====

Addon feature is testing right now, and each addon should has its own folder with ``__init__.py`` inside.

Addon folder struture shows like:

::

    $HOME
    └───Tsaotun
        └───addons
            ├── addon_A - __init__.py, ...
            ├── addon_B - __init__.py, ...
            └───__init__.py


Best practices (Sample addon to remove "ALL" containers at once, no matter it's dead or alive)
----------------------------------------------------------------------------------------------

**__init__.py: To specify how to override the original command**

.. code-block:: python

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


**Container/rm.py**

.. code-block:: python

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


Licence
=======

Apache License v2.0: `LICENSE <https://github.com/qazbnm456/tsaotun/blob/master/LICENSE>`_.


Author
======

`Boik Su`_  (`@qazbnm456`_) created Tsaotun.


.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _dockerhub: https://hub.docker.com/r/qazbnm456/tsaotun/
.. _VWGen: VWGen
.. _Boik Su: https://github.com/qazbnm456
.. _@qazbnm456: https://twitter.com/qazbnm456


.. |pypi| image:: https://img.shields.io/pypi/v/tsaotun.svg?style=flat-square&label=latest%20stable%20version
    :target: https://pypi.python.org/pypi/tsaotun
    :alt: Latest version released on PyPi

.. |unix_docker| image:: https://img.shields.io/badge/docker%20version-1.13.0-blue.svg
    :alt: Compatible on Linux

.. |mac_docker| image:: https://img.shields.io/badge/docker%20version-1.13.0-blue.svg
    :alt: Compatible on Mac

.. |windows_docker|  image:: https://img.shields.io/badge/docker%20version-1.13.0-blue.svg
    :alt: Compatible on Windows
