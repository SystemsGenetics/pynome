"""This is the setup script for Pynome.

It should install Pynome on the local system / environment.

"""


from setuptools import setup, find_packages


# A good blog entry on entry points:
# http://amir.rachum.com/blog/2017/07/28/python-entry-points/
# Run the setup function to install the program.

setup(
    name='pynome'
    ,version='0.999'
    ,packages=find_packages()
    ,entry_points = {
        'console_scripts': ['pynome = pynome.__main__:main']
    }
)
