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
    for filename in os.listdir("."):
        if filename.endswith("_example.py"):
            exec(open(filename).read())
