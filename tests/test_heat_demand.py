"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

import matplotlib


def test_heat_example():
    """Test the results of the heat example."""
    matplotlib.use("Agg")
    from demandlib.examples import heat_demand_example
