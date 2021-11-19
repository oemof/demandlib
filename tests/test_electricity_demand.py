"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

import matplotlib


def test_power_example():
    matplotlib.use("Agg")
    import demandlib_examples.power_demand_example  # noqa: F401
