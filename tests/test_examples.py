"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

import os
from unittest.mock import patch

from matplotlib import use


@patch("matplotlib.pyplot.show")
def test_examples(capsys):
    """Test the results of the heat example."""
    use("agg")
    path = os.path.join(os.path.dirname(__file__), os.pardir, "examples")
    os.chdir(path)
    for filename in os.listdir(path):
        if filename.endswith("_example.py"):
            fn = os.path.join(path, filename)
            with open(fn, "r") as f:
                exec(f.read())
