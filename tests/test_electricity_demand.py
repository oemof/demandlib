"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

import matplotlib
# import numpy as np


def test_power_example():
    matplotlib.use("Agg")
    import demandlib.examples.power_demand_example  # noqa: F401
