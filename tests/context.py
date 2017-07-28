# Module import framework for testing. From:
#
#    http://python-guide-pt-br.readthedocs.io/en/latest/writing/structure/
#
# From the individual test modules import with:
#
#     from .context import pynome
#

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pynome
