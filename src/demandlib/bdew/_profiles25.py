# -*- coding: utf-8 -*-
"""
Implementation of the 2025 BDEW standard load profiles:
* H25 (dynamic), household profile based on 2018 and 2019 data
* G25 (static), industrial profile based on 2022 and 2023 data
* L25 (static), farm profile based on previous L0 profile
* P25 (dynamic), profile for households with PV based on 2022 and 2023 data
* S25 (dynamic), profile for households with BES based on 2022 and 2023 data

SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd


_bdew_datapath = os.path.join(os.path.dirname(__file__), "bdew_data")

class BDEW25Profile(pd.Series):
    @property
    def datafile(self):
        raise NotImplementedError(
            "BDEW25Profile needs to be implemented,"
            " please use one of its children instead."
        )

    def __init__(self, timeindex: pd.DatetimeIndex):
        profile_data = pd.read_csv(_bdew_datapath + self.datafile)
        profile = profile_data
        super().__init__(data=profile, index=timeindex)


class L25(BDEW25Profile):
    def __init__(
            self,
            timeindex: pd.DatetimeIndex
    ):
        super().__init__(timeindex=timeindex)

    @property
    def datafile(self):
        return "/l25.csv"


if __name__ == "__main__":
    dti = pd.date_range("2018-01-01", periods=15, freq="15min")

    profile_data = pd.read_csv(_bdew_datapath + "/l25.csv", header=[0,1])

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

    print(profile_data)

    print(dti.month, dti.day_of_week)
