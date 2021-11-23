"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""
import os

import matplotlib


def test_examples():
    """Test the results of the heat example."""
    matplotlib.use("Agg")
    path = os.path.join(os.path.dirname(__file__), os.pardir, "examples")
    os.chdir(path)
    for filename in os.listdir(path):
        if filename.endswith("_example.py"):
            fn = os.path.join(path, filename)
            exec(open(fn).read())
