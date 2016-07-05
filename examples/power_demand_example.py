# -*- coding: utf-8 -*-
"""Creating power demand profiles using bdew profiles.
"""

import pandas as pd
from demandlib.demandlib import power_bdew as bdew
from oemof.tools import helpers
from matplotlib import pyplot as plt

year = 2013

ann_el_demand_per_sector = {
    'g0': 3000,
    'h0': 3000,
    'i0': 3000,
    'g6': 5000}

# create basic dataframe for a given year and include holidays optionally
dataframe = helpers.create_basic_dataframe(year)

# read standard load profiles
e_slp = bdew.bdew_elec_slp(dataframe).slp

# normalize slp timeseries to annual sum of one
e_slp.drop('date', axis=1, inplace=True)
e_slp = e_slp.div(e_slp.sum(axis=0), axis=1)

# multiply given annual demand with timeseries
elec_demand = e_slp.multiply(pd.Series(
    ann_el_demand_per_sector), axis=1).dropna(how='all',
                                              axis=1)

# Plot demand
ax = elec_demand.plot()
ax.set_xlabel("Date")
ax.set_ylabel("Power demand")
plt.show()
