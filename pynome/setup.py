from setuptools import setup

setup(
    name='Pynome',
    author='Tyler Biggs',
    author_email='biggstd@gmail.com',
    version='0.1.0',
    packages=['pynome'],
    entry_points={
        'console_scripts': [
            'pynome = pynome.pynome:main'
        ]
    },
    )
