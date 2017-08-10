# """
# Python __init__.py file denotes the folder it is in as a package.
# """

# import logging
# import logging.config

# # load the configuration file
# logging.config.fileConfig('pynome/pynomeLog.conf')
from pynome.genomedatabase import GenomeEntry, GenomeDatabase
from pynome.ensembldatabase import EnsemblDatabase