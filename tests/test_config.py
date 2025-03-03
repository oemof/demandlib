# -*- coding: utf-8 -*-

"""
Tests for the config module.

SPDX-FileCopyrightText: 2016-2021 Uwe Krien <uwe.krien@ifam.fraunhofer.de>

SPDX-License-Identifier: MIT
"""
__copyright__ = "Uwe Krien <uwe.krien@ifam.fraunhofer.de>"
__license__ = "MIT"


import os
from configparser import NoOptionError
from configparser import NoSectionError

import pytest

from demandlib import config


def test_ini_filenames_basic():
    files = config.get_ini_filenames()
    local_path = os.path.join(os.path.expanduser("~"), ".demandlib")
    fn = sorted([f.split(os.sep)[-1] for f in files if local_path not in f])
    assert fn == ["demandlib.ini"]


def test_ini_filenames_local_path():
    local_path = os.path.join(os.path.expanduser("~"), ".demandlib")
    os.makedirs(local_path, exist_ok=True)
    new_file = os.path.join(local_path, "test_ini_file_34RTXX.ini")
    f = open(new_file, "w+")
    f.close()
    files = config.get_ini_filenames()
    fn = sorted([f.split(os.sep)[-1] for f in files])
    assert "test_ini_file_34RTXX.ini" in fn
    os.remove(new_file)


def test_init_basic():
    assert config.get("tester", "test_entry") == 5
    config.init()
    local_path = os.path.join(os.path.expanduser("~"), ".demandlib")
    fn = sorted(
        [f.split(os.sep)[-1] for f in config.FILES if local_path not in f]
    )
    assert fn == ["demandlib.ini"]


def test_init_own_file_list():
    files = [
        os.path.join(os.path.dirname(__file__), "test_data", "config_test.ini")
    ]
    config.init(files=files)
    fn = sorted([f.split(os.sep)[-1] for f in config.FILES])
    assert fn == ["config_test.ini"]
    assert config.get("tester", "my_test") == "my_value"


def test_check_functions():
    files = [
        os.path.join(os.path.dirname(__file__), "test_data", "config_test.ini")
    ]
    config.init(files=files)
    assert config.has_section("tester")
    assert not (config.has_section("teste"))
    assert config.has_option("tester", "my_test")


def test_get_function():
    """Read config file."""
    files = [
        os.path.join(os.path.dirname(__file__), "test_data", "config_test.ini")
    ]
    config.init(files=files)
    assert config.get("type_tester", "my_bool")
    assert isinstance(config.get("type_tester", "my_int"), int)
    assert isinstance(config.get("type_tester", "my_float"), float)
    assert isinstance(config.get("type_tester", "my_string"), str)
    assert isinstance(config.get("type_tester", "my_None"), type(None))
    assert isinstance(config.get("type_tester", "my_list"), str)
    assert int(config.get_list("type_tester", "my_list")[2]) == 7


def test_missing_value():
    files = [
        os.path.join(os.path.dirname(__file__), "test_data", "config_test.ini")
    ]
    config.init(files=files)
    with pytest.raises(
        NoOptionError, match="No option 'blubb' in section: 'type_tester'"
    ):
        config.get("type_tester", "blubb")
    with pytest.raises(NoSectionError, match="No section: 'typetester'"):
        config.get("typetester", "blubb")


def test_dicts():
    """Test dictionaries in config file."""
    files = [
        os.path.join(os.path.dirname(__file__), "test_data", "config_test.ini")
    ]
    config.init(files=files)
    d = config.get_dict("type_tester")
    assert d["my_list"] == "4,6,7,9"
    d = config.get_dict_list("type_tester")
    assert d["my_list"][1] == "6"
    assert d["my_None"][0] is None
    assert d["my_int"][0] == 5
    d = config.get_dict_list("type_tester", string=True)
    assert d["my_list"][1] == "6"
    assert d["my_None"][0] == "None"
    assert d["my_int"][0] == "5"


def test_set_temp_value():
    files = [
        os.path.join(os.path.dirname(__file__), "test_data", "config_test.ini")
    ]
    config.init(files=files)
    with pytest.raises(
        NoOptionError, match="No option 'blubb' in section: 'type_tester'"
    ):
        config.get("type_tester", "blubb")
    config.tmp_set("type_tester", "blubb", "None")
    assert config.get("type_tester", "blubb") is None
    config.tmp_set("type_tester", "blubb", "5.5")
    assert config.get("type_tester", "blubb") == 5.5


def test_set_temp_without_init():
    config.tmp_set("type_tester", "blubb", "None")
