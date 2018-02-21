"""This is the setup script for Pynome.

It should install Pynome on the local system / environment.

"""


from setuptools import setup, find_packages


# A good blog entry on entry points:
# http://amir.rachum.com/blog/2017/07/28/python-entry-points/
# Run the setup function to install the program.

setup(
    name='pynome',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'Click',
        'SQLAlchemy'
        'tqdm',
        'pandas',
        'xmltodict',
    ],
    entry_points={
        # Console scripts are those that can be run directly from the terminal.
        # String entries here will be the cli invocation for their corresponding
        # python modulefiles:functions.
        'console_scripts': [
            'pynome = pynome.cli:pynome',
        ]
    }
)
