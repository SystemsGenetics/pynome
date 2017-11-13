"""
Initialization module for pynome.
"""
__docformat__ = 'reStructuredText'  # Set the formatting for the documentation
from sqlalchemy.orm import sessionmaker

# Import this in other packages with:
# >>> from pynome import Session
Session = sessionmaker()
