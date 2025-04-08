"""
SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt
SPDX-FileCopyrightText: Patrik Schönfeldt


SPDX-License-Identifier: MIT
"""

import datetime

import matplotlib.pyplot as plt
import pandas as pd


from demandlib import bdew

dt_index = pd.date_range(
    start="2020-01-01 00:00",
    end="2020-01-31 23:45",
    freq="15min",
)

holidays = [
    datetime.date(2020, 1, 1),
    datetime.date(2020, 1, 2),
    datetime.date(2020, 1, 3),
    datetime.date(2020, 1, 4),
    datetime.date(2020, 1, 5),
]

h25_holidays = bdew.H25(dt_index, holidays)
h25 = bdew.H25(dt_index)

print(h25.sum() / 4)
print(h25_holidays.sum() / 4)

plt.plot(h25, label="HWD")
plt.plot(h25_holidays, label="HHD")
plt.legend()

plt.show()
