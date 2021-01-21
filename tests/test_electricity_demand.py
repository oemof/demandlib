"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT

"""

from demandlib.examples import power_demand_example


def test_power_example():
    """Test the results of the power example."""
    assert int(power_demand_example.power_example(True).sum().sum()) == 24999
