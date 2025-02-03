# -*- coding: utf-8 -*-
"""
Implementation of the standard load profiles

SPDX-FileCopyrightText: Birgit Schachler
SPDX-FileCopyrightText: Uwe Krien <krien@uni-bremen.de>
SPDX-FileCopyrightText: jnnr
SPDX-FileCopyrightText: Stephen Bosch
SPDX-FileCopyrightText: Patrik Schönfeldt

SPDX-License-Identifier: MIT
"""
import calendar
import datetime
import os

import pandas as pd

from demandlib.tools import add_weekdays2df


class ElecSlp:
    """Generate electrical standardized load profiles based on the BDEW method.

    Attributes
    ----------
    datapath : string
        Path to the csv files containing the load profile data.
    date_time_index : pandas.DateTimeIndex
        Time range for and frequency for the profile.

    Parameters
    ----------
    year : integer
        Year of the demand series.

    Optional Parameters
    -------------------
    seasons : dictionary
        Describing the time ranges for summer, winter and transition periods.
    holidays : dictionary or list
        The keys of the dictionary or the items of the list should be datetime
        objects of the days that are holidays.
    """

    def __init__(self, year, seasons=None, holidays=None):
        if calendar.isleap(year):
            hoy = 8784
        else:
            hoy = 8760
        self.datapath = os.path.join(os.path.dirname(__file__), "bdew_data")
        self.date_time_index = pd.date_range(
            datetime.datetime(year, 1, 1, 0), periods=hoy * 4, freq="15Min"
        )
        if seasons is None:
            self.seasons = {
                "summer1": [5, 15, 9, 14],  # summer: 15.05. to 14.09
                "transition1": [3, 21, 5, 14],  # transition1 :21.03. to 14.05
                "transition2": [9, 15, 10, 31],  # transition2 :15.09. to 31.10
                "winter1": [1, 1, 3, 20],  # winter1:  01.01. to 20.03
                "winter2": [11, 1, 12, 31],  # winter2: 01.11. to 31.12
            }
        else:
            self.seasons = seasons
        self.year = year
        # Create the default profiles
        self.slp_frame = self.all_load_profiles(
            self.date_time_index, holidays=holidays
        )
        # Add the dynamic H0 profile
        self.create_dynamic_h0_profile()

    def all_load_profiles(self, time_df, holidays=None):
        slp_types = [
            "h0",
            "g0",
            "g1",
            "g2",
            "g3",
            "g4",
            "g5",
            "g6",
            "l0",
            "l1",
            "l2",
        ]
        new_df = self.create_bdew_load_profiles(
            time_df, slp_types, holidays=holidays
        )

        return new_df

    def create_bdew_load_profiles(self, dt_index, slp_types, holidays=None):
        """
        Calculates the hourly electricity load profile in MWh/h of a region.
        """

        # define file path of slp csv data
        file_path = os.path.join(self.datapath, "selp_series.csv")

        # Read standard load profile series from csv file
        selp_series = pd.read_csv(file_path)
        tmp_df = selp_series
        # Create an index to merge. The year and month will be ignored only the
        # time index is necessary.
        index = pd.date_range(
            datetime.datetime(2007, 1, 1, 0), periods=2016, freq="15Min"
        )
        tmp_df.set_index(index, inplace=True)

        # Create empty DataFrame to take the results.
        new_df = pd.DataFrame(
            index=dt_index, columns=slp_types, dtype=float
        ).fillna(0)
        new_df = add_weekdays2df(
            new_df, holidays=holidays, holiday_is_sunday=True
        )

        new_df["hour"] = dt_index.hour.astype("int64")
        new_df["weekday"] = new_df["weekday"].astype("int64")
        new_df["minute"] = dt_index.minute.astype("int64")
        time_df = new_df[["date", "hour", "minute", "weekday"]].copy()
        tmp_df[slp_types] = tmp_df[slp_types].astype(float)

        # Inner join the slps on the time_df to the slp's for a whole year
        tmp_df["hour_of_day"] = tmp_df.index.hour
        tmp_df["minute_of_hour"] = tmp_df.index.minute
        left_cols = ["hour_of_day", "minute_of_hour", "weekday"]
        right_cols = ["hour", "minute", "weekday"]
        tmp_df = tmp_df.reset_index(drop=True)

        for p in self.seasons.keys():
            a = datetime.datetime(
                self.year, self.seasons[p][0], self.seasons[p][1], 0, 0
            )
            b = datetime.datetime(
                self.year, self.seasons[p][2], self.seasons[p][3], 23, 59
            )
            merged_df = pd.DataFrame.merge(
                tmp_df[tmp_df["period"] == p[:-1]],
                time_df[a:b],
                left_on=left_cols,
                right_on=right_cols,
                how="inner",
            ).drop(labels=["hour_of_day"], axis=1)

            merged_df.index = (
                pd.to_datetime(merged_df["date"])
                + pd.to_timedelta(merged_df["hour"], unit="h")
                + pd.to_timedelta(merged_df["minute"], unit="m")
            )
            merged_df.sort_index(inplace=True)

            new_df.update(merged_df)

        new_df.drop(
            ["date", "minute", "hour", "weekday"], axis=1, inplace=True
        )
        return new_df.div(new_df.sum(axis=0), axis=1)

    def create_dynamic_h0_profile(self):
        """
        Use the dynamisation function of the BDEW to smoothen the seasonal
        edges. Functions resolution is daily.

            .. math::
                f(x) = -3.916649251 * 10^-10 * x^4 + 3.2 * 10^-7 * x^3 - 7.02
                * 10^-5 * x^2+0.0021 * x + 1.24

        Adjustment of accuracy: from -3,92 to -3.916649251
        """
        # Create a Series with the day of the year as decimal number
        decimal_day = pd.Series(
            [((q + 1) / (24 * 4)) for q in range(len(self.slp_frame))],
            index=self.slp_frame.index,
        )

        # Calculate the smoothing factor of the BDEW dynamic H0 profile
        smoothing_factor = (
            -3.916649251 * 10**-10 * decimal_day**4
            + 3.2 * 10**-7 * decimal_day**3
            - 7.02 * 10**-5 * decimal_day**2
            + 0.0021 * decimal_day
            + 1.24
        )

        # Multiply the smoothing factor with the default H0 profile
        self.slp_frame["h0_dyn"] = self.slp_frame["h0"].mul(smoothing_factor)
        return self.slp_frame["h0_dyn"]

    def get_profile(self, ann_el_demand_per_sector):
        """Get the profiles for the given annual demand

        Parameters
        ----------
        ann_el_demand_per_sector : dictionary
            Key: sector, value: annual value

        Returns
        -------
        pandas.DataFrame : Table with all profiles

        """
        return (
            self.slp_frame.multiply(
                pd.Series(ann_el_demand_per_sector), axis=1
            ).dropna(how="all", axis=1)
            * 4
        )
