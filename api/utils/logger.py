#!/usr/bin/env python

"""
         DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
                Version 2, December 2004

 Copyright (C) 2015 Thomas Maurice <thomas@maurice.fr>

 Everyone is permitted to copy and distribute verbatim or modified
 copies of this license document, and changing it is allowed as long
 as the name is changed.

            DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
   TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION

  0. You just DO WHAT THE FUCK YOU WANT TO.
"""

import logging

def setup_logger(name, to_stdout=True, file_name=None):
    """Creates the logging object used by the script

    By defaults it prints information ton stdout, but
    you can tell it to print out information ton a file too
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    )

    # reset handlers
    for handler in logger.handlers:
        # Don't close stdout or stderr !
        if handler.__class__ != logging.StreamHandler:
            handler.stream.close()
        logger.removeHandler(handler)

    if file_name:
        fhandle = logging.FileHandler(file_name)
        fhandle.setLevel(logging.DEBUG)
        fhandle.setFormatter(formatter)
        logger.addHandler(fhandle)

    if to_stdout:
        chandle = logging.StreamHandler()
        chandle.setLevel(logging.DEBUG)
        chandle.setFormatter(formatter)
        logger.addHandler(chandle)

    return logger
