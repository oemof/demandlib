# -*- coding: utf-8 -*-
"""
Implementation of the 2025 BDEW standard load profiles:
* G25 (static), industrial profile based on 2022 and 2023 data
* H25 (dynamic), household profile based on 2018 and 2019 data
* L25 (static), farm profile based on previous L0 profile
* P25 (dynamic), profile for households with PV based on 2022 and 2023 data
* S25 (dynamic), profile for households with BES based on 2022 and 2023 data

SPDX-FileCopyrightText: Deutsches Zentrum für Luft- und Raumfahrt
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import os

import numpy as np
import pandas as pd

from demandlib.tools import set_holidays_in_df

_bdew_datapath = os.path.join(os.path.dirname(__file__), "bdew_data")


class BDEW25Profile(pd.Series):
    def __init__(
        self, timeindex: pd.DatetimeIndex, holidays: dict | list | None = None
    ):
        if timeindex.freq.delta != pd.Timedelta("00:15:00"):
            raise NotImplementedError(
                "BDEW time series are only implemented for 15-minute steps."
                " Please give corresponding index."
            )
        new_df = pd.DataFrame(
            data={
                "month": timeindex.month,
                "weekday": timeindex.day_of_week + 1,
                "hour": timeindex.hour,
                "minute": timeindex.minute,
            },
            index=timeindex,
        )

        set_holidays_in_df(new_df, holidays=holidays)

        new_df.replace({"weekday": [1, 2, 3, 4, 5]}, "WT", inplace=True)
        new_df.replace({"weekday": [6]}, "SA", inplace=True)
        new_df.replace(
            {"weekday": [0, 7]}, "FT", inplace=True
        )  # 0 for holiday

        new_df = new_df.merge(
            self.raw_profile_data,
            on=["month", "weekday", "hour", "minute"],
            how="inner",
        )
        new_df.set_index(timeindex, inplace=True)

        super().__init__(data=new_df.value, index=timeindex)

    @property
    def datafile(self):
        raise NotImplementedError(
            "BDEW25Profile needs to be implemented,"
            " please use one of its children instead."
        )

    @property
    def raw_profile_data(self):
        profile_data = pd.read_csv(
            _bdew_datapath + self.datafile,
            header=[0, 1],
        )

        profile_data.rename(
            columns={
                "Januar": 1,
                "Februar": 2,
                "März": 3,
                "April": 4,
                "Mai": 5,
                "Juni": 6,
                "Juli": 7,
                "August": 8,
                "September": 9,
                "Oktober": 10,
                "November": 11,
                "Dezember": 12,
            },
            inplace=True,
        )
        del profile_data[("Unnamed: 0_level_0", "[kWh]")]

        hours = [h for h in range(24) for _ in range(4)]
        minutes = [m for _ in range(24) for m in range(0, 60, 15)]
        serialised_data = []
        for column in profile_data.columns:
            serialised_data.append(
                pd.DataFrame(
                    data={
                        "month": column[0],
                        "weekday": column[1],
                        "hour": hours,
                        "minute": minutes,
                        "value": 4 * profile_data[column],
                    }
                )
            )

        profile_data = pd.concat(serialised_data, ignore_index=True)
        return profile_data


class DynamicBDEW25Profile(BDEW25Profile):
    def __init__(
        self, timeindex: pd.DatetimeIndex, holidays: dict | list | None = None
    ):
        super().__init__(timeindex=timeindex, holidays=holidays)
        self.update(self * self.dynamisation_function(timeindex))

    @staticmethod
    def dynamisation_function(timeindex: pd.DatetimeIndex) -> pd.Series:

        # cast to float hear because of miscalculations when using integers
        day_of_year = np.array(timeindex.day_of_year, dtype=float)

        return pd.Series(
            -3.92 * 10**-10 * day_of_year**4
            + 3.2 * 10**-7 * day_of_year**3
            - 7.02 * 10**-5 * day_of_year**2
            + 0.0021 * day_of_year
            + 1.24,
            index=timeindex,
        )


class G25(BDEW25Profile):
    def __init__(
        self, timeindex: pd.DatetimeIndex, holidays: dict | list | None = None
    ):
        super().__init__(timeindex=timeindex, holidays=holidays)

    @property
    def datafile(self):
        return "/g25.csv"


class H25(DynamicBDEW25Profile):
    def __init__(
        self, timeindex: pd.DatetimeIndex, holidays: dict | list | None = None
    ):
        super().__init__(timeindex=timeindex, holidays=holidays)

    @property
    def datafile(self):
        return "/h25.csv"


class L25(BDEW25Profile):
    def __init__(
        self, timeindex: pd.DatetimeIndex, holidays: dict | list | None = None
    ):
        super().__init__(timeindex=timeindex, holidays=holidays)

    @property
    def datafile(self):
        return "/l25.csv"


class P25(DynamicBDEW25Profile):
    def __init__(
        self, timeindex: pd.DatetimeIndex, holidays: dict | list | None = None
    ):
        super().__init__(timeindex=timeindex, holidays=holidays)

    @property
    def datafile(self):
        return "/p25.csv"


class S25(DynamicBDEW25Profile):
    def __init__(
        self, timeindex: pd.DatetimeIndex, holidays: dict | list | None = None
    ):
        super().__init__(timeindex=timeindex, holidays=holidays)

    @property
    def datafile(self):
        return "/s25.csv"
