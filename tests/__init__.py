"""__init__ module for pynome tests.

This module sets up the logger for use in testing Pynome.
"""

import logging
import logging.config

# Configure the logger.
logging.basicConfig(
    filename='pynome_test.log',
    filemode='w',
    format='%(levelname)s:\t%(name)s\t%(message)s',
    level=logging.DEBUG)

# For testing this logger:
# logger = logging.getLogger(__name__)
#
#
# # Test the created logger.
# logger.debug('debug message')
# logger.info('info message.')
# logger.warning('warn message.')
# logger.error('error message.')
# logger.critical('critical message.')
