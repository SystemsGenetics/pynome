"""
Contains all core classes, functions, and objects of this application.
"""

from ._assembly import Assembly
from ._log import Log


#
# The singleton instance of the assembly class.
#
assembly = Assembly()


#
# The singleton instance of the log class.
#
log = Log()
