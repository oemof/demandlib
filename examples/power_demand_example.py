# -*- coding: utf-8 -*-
"""Creating power demand profiles using bdew profiles.
"""

import datetime
import demandlib.bdew as bdew
import demandlib.particular_profiles as profiles
from datetime import time as settime
from matplotlib import pyplot as plt

year 2010

# The following dictionary is create by "workalendar"
# pip3 install workalendar
# >>> from workalendar.europe import Germany
# >>> cal = Germany()
# >>> holidays = dict(cal.holidays(2010))
holidays = {
    datetime.date(2010, 5, 24): 'Whit Monday',
    datetime.date(2010, 4, 5): 'Easter Monday',
    datetime.date(2010, 5, 13): 'Ascension Thursday',
    datetime.date(2010, 1, 1): 'New year',
    datetime.date(2010, 10, 3): 'Day of German Unity',
    datetime.date(2010, 12, 25): 'Christmas Day',
    datetime.date(2010, 5, 1): 'Labour Day',
    datetime.date(2010, 4, 2): 'Good Friday',
    datetime.date(2010, 12, 26): 'Second Christmas Day'}

ann_el_demand_per_sector = {
    'g0': 3000,
    'h0': 3000,
    'i0': 3000,
    'i1': 5000,
    'i2': 6000,
    'g6': 5000}

# read standard load profiles
e_slp = bdew.ElecSlp(year, holidays=holidays)

# multiply given annual demand with timeseries
elec_demand = e_slp.get_profile(ann_el_demand_per_sector)

# Add the slp for the industrial group

ilp = profiles.IndustrialLoadProfile(e_slp.date_time_index, holidays=holidays)
elec_demand['i0'] = ilp.simple_profile(ann_el_demand_per_sector['i0'])

# Resample 15-minute values to hourly values.
elec_demand = elec_demand.resample('H').mean() * 4

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

# Plot demand
ax = elec_demand.plot()
ax.set_xlabel("Date")
ax.set_ylabel("Power demand")
plt.show()
