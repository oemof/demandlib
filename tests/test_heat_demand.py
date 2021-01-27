"""
Test the electricity demand

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT

"""

import numpy as np

from demandlib.examples import heat_demand_example


def test_heat_example():
    """Test the results of the heat example."""
    ann_demands_per_type = {'efh': 25000,
                            'mfh': 80000,
                            'ghd': 140000}

    demands = heat_demand_example.heat_example(
        ann_demands_per_type=ann_demands_per_type,
        testmode=True).sum()

    for key in ann_demands_per_type:
        assert np.isclose(demands[key], ann_demands_per_type[key], rtol=1e-4)
