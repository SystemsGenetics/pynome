"""
Contains all global setting for this application.
"""
import os








JOB_NAME = "pynome_work_%05d.txt"
cpuCount = os.cpu_count()
rootPath = os.path.join(os.path.expanduser("~"),"species")
