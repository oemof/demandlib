# -*- coding: utf-8 -*-
"""Creating power demand profiles using bdew profiles.
"""

import pandas as pd
import demandlib.bdew as bdew
import demandlib.particular_profiles as profiles
from datetime import time as settime
from matplotlib import pyplot as plt

year = 2013

ann_el_demand_per_sector = {
    'g0': 3000,
    'h0': 3000,
    'i0': 3000,
    'i1': 5000,
    'i2': 6000,
    'g6': 5000}

# create basic dataframe for a given year and include holidays optionally
dataframe_index = pd.date_range(pd.datetime(year, 1, 1, 0), periods=8760,
                                freq='H')

# read standard load profiles
e_slp = bdew.ElecSlp(dataframe_index)

# multiply given annual demand with timeseries
elec_demand = e_slp.get_profile(ann_el_demand_per_sector)

# Add the slp for the industrial group
ilp = profiles.IndustrialLoadProfile(dataframe_index)

# Beginning and end of workday, weekdays and weekend days, and scaling factors
# by default
elec_demand['i0'] = ilp.simple_profile(ann_el_demand_per_sector['i0'])

# Set beginning of workday to 9 am
elec_demand['i1'] = ilp.simple_profile(ann_el_demand_per_sector['i1'],
                                       am=settime(9, 0, 0))

# Change scaling factors
elec_demand['i2'] = ilp.simple_profile(ann_el_demand_per_sector['i2'],
                                       profile_factors={'week':
                                                        {'day': 1.0,
                                                         'night': 0.8},
                                                        'weekend':
                                                        {'day': 0.8,
                                                         'night': 0.6}})

# Plot demand
ax = elec_demand.plot()
ax.set_xlabel("Date")
ax.set_ylabel("Power demand")
plt.show()
