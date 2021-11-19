"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

import numpy as np

from demandlib.examples import power_demand_example


def test_power_example():
    """Test the results of the power example."""

    ann_el_demands_per_sector = {
        "g0": 3000,
        "h0": 3000,
        "i0": 3000,
        "i1": 5000,
        "i2": 6000,
        "g6": 5000,
    }

    demands = (
        power_demand_example.power_example(
            ann_el_demand_per_sector=ann_el_demands_per_sector, testmode=True
        ).sum()
        / 4
    )

    for key in ann_el_demands_per_sector:
        assert np.isclose(demands[key], ann_el_demands_per_sector[key])
