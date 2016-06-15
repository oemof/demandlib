# -*- coding: utf-8 -*-
"""Creating heat demand profiles using the bdew method.
"""

import pandas as pd
from demandlib import bdew
from oemof.tools import helpers
from matplotlib import pyplot as plt

# read example temperature series
temperature = pd.read_csv("example_data.csv")["temperature"]
year = 2010

# get german holidays
holidays = helpers.get_german_holidays(year, ['Germany', 'SH'])

demand = pd.DataFrame(index=bdew.HeatBuilding(year).df.index)

demand['efh'] = bdew.HeatBuilding(
    year, holidays=holidays, temperature=temperature, shlp_type='EFH',
    building_class=1, wind_class=1, annual_heat_demand=25000, name='EFH'
    ).get_bdew_profile()

demand['mfh'] = bdew.HeatBuilding(
    year, holidays=holidays, temperature=temperature, shlp_type='MFH',
    building_class=2, wind_class=0, annual_heat_demand=80000, name='MFH'
    ).get_bdew_profile()

# Plot demand of building
ax = demand.plot()
ax.set_xlabel("Date")
ax.set_ylabel("Heat demand in MW")
plt.show()
