#!/usr/bin/env python

import os

from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

requirements = [
    'docker >= 2.0.0',
    'dockerpty >= 0.4.1',
    'arrow >= 0.10.0',
    'humanize >= 0.5.1',
    'pystache >= 0.5.4',
    'colorama >= 0.3.7'
]

version = None
exec(open('version.py').read())

setup(name='dokcer',
      version=version,
      description='Python based Assistance for Docker',
      author='Boik Su',
      author_email='boik@tdohacker.org',
      url='https://github.com/qazbnm456/dokcer',
      packages=find_packages(),
      install_requires=requirements
     )
