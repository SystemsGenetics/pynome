# -*- coding: utf-8 -*-

"""
============
Pynome Setup
============



"""

from setuptools import setup, find_packages

setup(
    name='pynome',
    author='Tyler Biggs',
    author_email='biggstd@gmail.com',
    version='0.1',
    packages=find_packages(exclude=['tests']),
    py_modules=['pynome'],
    install_requires=[
        'Click',
        'pandas',
        'ftplib',
    ],
    entry_points={
        'console_scripts': [
            'pynome = pynome.cli:entry_point'
        ]
    },
)
