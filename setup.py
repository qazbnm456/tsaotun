"""python setup script"""
import codecs
import os
import re

from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)


def find_version(*file_paths):
    """
    Read the version number from a source file.
    Why read it, and not import?
    see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
    """
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(ROOT_DIR, *file_paths), 'r', 'latin1') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')

requirements = [
    'docker >= 2.0.0',
    'dockerpty >= 0.4.1',
    'arrow >= 0.10.0',
    'humanize >= 0.5.1',
    'pystache >= 0.5.4',
    'colorama >= 0.3.7',
    'argcomplete >= 1.7.0'
]

setup(name='dokcer',
      version=find_version('dokcer', '__init__.py'),
      description='Python based Assistance for Docker',
      author='Boik Su',
      author_email='boik@tdohacker.org',
      url='https://github.com/qazbnm456/dokcer',
      download_url='https://codeload.github.com/qazbnm456/dokcer/tar.gz/0.5',
      keywords=['0.5'],
      packages=find_packages(),
      install_requires=requirements,
      entry_points="""
            [console_scripts]
            dokcer=dokcer.cli:cli
      """,
      classifiers=[
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Topic :: Software Development',
          'Topic :: Terminals',
          'Topic :: Utilities',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7'
      ]
     )
