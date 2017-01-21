"""python setup script"""
import codecs
import os
import re
import shutil
import platform

from setuptools import (setup, find_packages)
from setuptools.command.install import install

ROOT_DIR = os.path.dirname(__file__)


class PostInstallCommand(install):
    """Post-installation for installation mode"""

    def run(self):
        install.run(self)
        print "Installing auto completion of tsaotun to",
        src = os.path.join(ROOT_DIR, 'completion', 'tsaotun')
        sys = platform.system()
        try:
            if sys == 'Darwin':
                dest = os.path.join(
                    os.popen('brew --prefix').read()[:-1], 'etc', 'bash_completion.d', 'tsaotun')
                print dest
                shutil.copy(src, dest)
            elif sys == 'Linux':
                dest = os.path.join(
                    '/etc', 'bash_completion.d', 'tsaotun')
                print dest
                shutil.copy(src, dest)
            else: # Windows, etc.
                print "... \n Warning: {} is currently not supported. Skipped.".format(sys)
        except IOError:
            print "Permission denied: You probably want to copy '{}' to '{}' manually.".format(src, dest)
        print "Tsaotun is installed successfully."


def find_version(*file_paths):
    """
    Read the version number from a source file.
    Why read it, and not import?
    see https://groups.google.com/d/topic/pypa-dev/0PkjVpcxTzQ/discussion
    """
    # Open in Latin-1 so that we avoid encoding errors.
    # Use codecs.open for Python 2 compatibility
    with codecs.open(os.path.join(ROOT_DIR, *file_paths), 'r', 'utf-8') as f:
        version_file = f.read()

    # The version line must have the form
    # __version__ = 'ver'
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string')


def read_requirements(requirements):
    """Read the requirements from a requirements txt file"""
    try:
        with codecs.open(os.path.join(ROOT_DIR, requirements), 'r', 'utf-8') as f:
            return f.read().splitlines()
    except IOError:
        raise IOError(os.getcwd())

# Get the long description from the relevant file
with codecs.open(os.path.join(ROOT_DIR, 'README.rst'), 'r', 'utf-8') as f:
    long_description = f.read()

setup(name='tsaotun',
      version=find_version('tsaotun', '__init__.py'),
      description='Python based Assistance for Docker',
      long_description=long_description,
      author='Boik Su',
      author_email='boik@tdohacker.org',
      url='https://github.com/qazbnm456/tsaotun',
      download_url='https://codeload.github.com/qazbnm456/tsaotun/tar.gz/0.9.2',
      keywords=['0.9.2'],
      packages=find_packages(),
      install_requires=read_requirements('requirements.txt'),
      entry_points="""
            [console_scripts]
            tsaotun=tsaotun.cli:cli
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
      ],
      cmdclass={
          'install': PostInstallCommand,
      }
     )
