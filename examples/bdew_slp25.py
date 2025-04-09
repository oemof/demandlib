"""
SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt
SPDX-FileCopyrightText: Patrik Schönfeldt


SPDX-License-Identifier: MIT
"""

import datetime

import matplotlib.pyplot as plt
import pandas as pd


from demandlib import bdew

index15m = pd.date_range(
    start="2020-01-01 00:00",
    end="2020-01-31 23:45",
    freq="15min",
)
index1m = pd.date_range(
    start="2020-01-01 00:00",
    end="2020-01-31 23:45",
    freq="1min",
)
index3h = pd.date_range(
    start="2020-01-01 00:00",
    end="2020-01-31 23:45",
    freq="3h",
)

holidays = [
    datetime.date(2020, 1, 1),
    datetime.date(2020, 1, 2),
    datetime.date(2020, 1, 3),
    datetime.date(2020, 1, 4),
    datetime.date(2020, 1, 5),
]

h25_holidays = bdew.H25(index1m, holidays)
h25_std = bdew.H25(index15m)
h25_3h = bdew.H25(index3h)

plt.step(h25_holidays.index, h25_holidays, label="Holidays", where="post")
plt.step(h25_std.index, h25_std, label="Standard", where="post")
plt.step(h25_3h.index, h25_3h, label="Three hours", where="post")
plt.legend()

plt.show()
