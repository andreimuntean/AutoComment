#!/usr/bin/python3

"""setup.py: Installs the modules required to run autocomment.py."""

__author__ = 'Alex Cristian, Andrei Muntean'
__license__ = 'MIT License'

from setuptools import setup


setup(
    name = 'AutoComment',
    version = '0.8.0',
    description = 'Replies to all timeline posts between two dates.',
    author = 'Alex Cristian, Andrei Muntean',
    license = 'MIT',
    keywords = 'facebook fb auto automatically comment reply',
    install_requires = ['facepy']
)