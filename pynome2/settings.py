"""
Contains all global setting for this application.
"""
import os


#
# Detailed description.
#
JOB_NAME = "pynome_work_%05d.job"


#
# The root path where the local species database is stored.
#
rootPath = os.path.join(os.path.expanduser("~"),"species")
