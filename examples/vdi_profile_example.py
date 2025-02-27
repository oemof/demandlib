# -*- coding: utf-8 -*-
"""
Creating heat and power demand profiles using VDI4655 profiles.

Installation requirements
-------------------------
This example requires at least version v0.1.4 of the oemof demandlib. Install
by:
    pip install 'demandlib>=0.1.4,<0.2'
Optional:
    pip install matplotlib

SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>

SPDX-License-Identifier: MIT

"""

import datetime

from matplotlib import pyplot as plt

from demandlib import vdi

# The following dictionary has been created by "workalendar"
# pip3 install workalendar
# from workalendar.europe import Germany
# cal = Germany()
# holidays = dict(cal.holidays(2017))

holidays = {
    datetime.date(2017, 1, 1): "New year",
    datetime.date(2017, 4, 14): "Good Friday",
    datetime.date(2017, 4, 17): "Easter Monday",
    datetime.date(2017, 5, 1): "Labour Day",
    datetime.date(2017, 5, 25): "Ascension Thursday",
    datetime.date(2017, 6, 5): "Whit Monday",
    datetime.date(2017, 10, 3): "Day of German Unity",
    datetime.date(2017, 10, 31): "Reformation Day",
    datetime.date(2017, 12, 25): "Christmas Day",
    datetime.date(2017, 12, 26): "Second Christmas Day",
}


my_houses = []
for n in range(2):
    my_houses.append(
        {
            "N_Pers": 3,
            "name": "EFH_{0}".format(n),
            "N_WE": 1,
            "Q_Heiz_a": 6000,
            "copies": 24,
            "house_type": "EFH",
            "Q_TWW_a": 1500,
            "W_a": 5250,
            "summer_temperature_limit": 15,
            "winter_temperature_limit": 5,
        }
    )
    my_houses.append(
        {
            "N_Pers": 45,
            "name": "MFH_{0}".format(n),
            "N_WE": 15,
            "Q_Heiz_a": 60000,
            "copies": 24,
            "house_type": "MFH",
            "Q_TWW_a": 15000,
            "W_a": 45000,
            "summer_temperature_limit": 15,
            "winter_temperature_limit": 5,
        }
    )

start = datetime.datetime.now()

# To get the DWD TRY region from coordinates the geopandas package is needed.
# pip3 install geopandas
# try_region = vdi.find_try_region(13.42, 52.82)
try_region = 4

# define the region
my_region = vdi.Region(
    2017,
    holidays=holidays,
    try_region=try_region,
    houses=my_houses,
    resample_rule="15min",
)

# calculate load profiles
lc = my_region.get_load_curve_houses()

print(datetime.datetime.now() - start)
lc = lc.T.groupby(level=[1, 2]).sum().T
lc = lc.rolling(15).mean()
print(datetime.datetime.now() - start)
print(lc)

lc.plot()
print(lc.sum())
plt.show()
