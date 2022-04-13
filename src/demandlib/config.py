# -*- coding: utf-8 -*-

"""
Adaptable config reader.

By default the config file of the package is used. Each value can be
overwritten with a user value with a custom config file in the $HOME directory
or in the working directory. The name of the config file must be:
demandlib.ini. If there is such a file in both locations the file in the
working directory will overwrite the one in the home folder.

SPDX-FileCopyrightText: Steffen - https://github.com/steffenGit
SPDX-FileCopyrightText: 2016-2021 Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT
"""

__all__ = [
    "get",
    "init",
]


import configparser as cp
import os

BLACKLIST = ["tox.ini"]

cfg = cp.RawConfigParser()
cfg.optionxform = str
_loaded = False


def get_ini_filenames():
    """Returns a list of ini files to use."""
    paths = []
    files = []

    paths.append(os.path.join(os.path.dirname(__file__)))
    paths.append(os.path.join(os.path.expanduser("~")))
    paths.append(os.getcwd())


    for p in paths:
        if p == "":  # Empty path string must be ignored
            continue
        for f in os.listdir(p):
            if f == "demandlib.ini":
                files.append(os.path.join(p, f))
    return files


def init():
    """Read config file(s)."""
    cfg.read(get_ini_filenames(), encoding="utf-8")
    global _loaded
    _loaded = True


def load():
    if not _loaded:
        init()


def get(section, key):
    """Returns the value of a given key in a given section."""
    load()
    try:
        return cfg.getint(section, key)
    except ValueError:
        try:
            return cfg.getfloat(section, key)
        except ValueError:
            try:
                return cfg.getboolean(section, key)
            except ValueError:
                value = cfg.get(section, key)
                if value == "None":
                    value = None
                return value
