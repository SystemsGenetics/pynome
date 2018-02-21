"""This module contains utilities for Pynome not specific to any class.

.. module:: untils
    :platform: Unix
    :synopsis: Functions that are needed by Pynome, but are not specific
    to any class or module.

..moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# Import general Python packages.
import os
import json
import logging
from sqlalchemy import create_engine


def read_json_config(config_file='pynome_config.json'):
    """Reads a json config file for required variables.
    """

    # Open the file, get the informaiton, then close it.
    with open(config_file) as cfg:
        config_dict = json.load(cfg)

    # Return the loaded configuration dictionary.
    return config_dict


def crawl_ftp_dir(ftp, top_dir, parsing_function, ignored_dirs):
    """Recursively crawl a target directory. Takes as an input a
    target directory and a parsing function. The ftplib.FTP.dir()
    function is used to retrieve a directory listing, line by line,
    in string format. These are appended to a newly generated list.
    Each item in this list is subject to the parsing function.

    :param database:
        An instance of ftplib.FTP()

    :param top_dir:
        The directory from which contents will be retrieved.

    :param parsing_function:
        The function to parse each non-directory result.

    """
    logging.debug(f'Top dir: {top_dir}')

    # Create an empty list to hold the callback
    retrieved_dir_list = []

    # The last argument passed to ftplib.dir acts as a callback if it
    # is a function. In this case the given function is a call to
    # append() the retrieved directory list.
    ftp.dir(top_dir, retrieved_dir_list.append)

    # For each line / directory listing retrieved.
    for line in retrieved_dir_list:

        # Split the line by whitespace.
        split_line = line.split()

        # Check if this entry is a directory.
        if split_line[0][0] == 'd':

            # If so, ensure it is not one of the dirs to be ignored.
            if split_line[-1] in ignored_dirs:

                # If this is the case, simply ignore this entry and
                # continue on this loop listing.
                continue

            # Otherwise this is a valid directory to start a new crawl in.
            else:

                # Construct the new top directory to start a crawl.
                target_dir = ''.join((top_dir, line.split()[-1], '/'))
                # Start a new crawl at this directory.
                crawl_ftp_dir(ftp, target_dir, parsing_function, ignored_dirs)

        # Check to make sure the filename is not on the 'bad list'
        # elif any(bw in split_line[-1] for bw in bad_words):
        #     continue

        # Otherwise the line is not a directory, and must be parsed.
        else:
            parsing_function(line, top_dir)
