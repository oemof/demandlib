# -*- coding: utf-8 -*-
"""
Implementation of the bdew standard load profiles for electric power.


"""
import logging
from datetime import time as settime

import pandas as pd

from .tools import add_weekdays2df


class IndustrialLoadProfile:
    """Generate an industrial heat or electric load profile."""

    def __init__(self, dt_index, holidays=None):
        self.dataframe = pd.DataFrame(index=dt_index)
        self.dataframe = add_weekdays2df(
            self.dataframe, holiday_is_sunday=True, holidays=holidays
        )

    def simple_profile(self, annual_demand, **kwargs):
        """
        Create industrial load profile

        Parameters
        ----------
        annual_demand : float
            Total demand.

        Other Parameters
        ----------------
        am : datetime.time
            beginning of workday
        pm : datetime.time
            end of workday
        week : list
            list of weekdays
        weekend : list
            list of weekend days
        profile_factors : dictionary
            dictionary with scaling factors for night and day of weekdays and
            weekend days
        """

        # Day(am to pm), night (pm to am), week day (week),
        # weekend day (weekend)
        am = kwargs.get("am", settime(7, 00, 0))
        pm = kwargs.get("pm", settime(23, 30, 0))

        week = kwargs.get("week", [1, 2, 3, 4, 5])
        weekend = kwargs.get("weekend", [0, 6, 7])

        default_factors = {
            "week": {"day": 0.8, "night": 0.6},
            "weekend": {"day": 0.9, "night": 0.7},
        }

        profile_factors = kwargs.get("profile_factors", default_factors)

        self.dataframe["ind"] = 0.0
        day_mask = self.dataframe.index.indexer_between_time(am, pm)
        night_mask = self.dataframe.index.indexer_between_time(pm, am)
        day_filter = pd.Series(False, index=self.dataframe.index)
        day_filter.iloc[day_mask] = True
        night_filter = pd.Series(False, index=self.dataframe.index)
        night_filter.iloc[night_mask] = True

        self.dataframe["ind"] = self.dataframe["ind"].mask(
            cond=day_filter & self.dataframe["weekday"].isin(week),
            other=profile_factors["week"]["day"],
        )
        self.dataframe["ind"] = self.dataframe["ind"].mask(
            cond=night_filter & self.dataframe["weekday"].isin(week),
            other=profile_factors["week"]["night"],
        )
        self.dataframe["ind"] = self.dataframe["ind"].mask(
            cond=day_filter & self.dataframe["weekday"].isin(weekend),
            other=profile_factors["weekend"]["day"],
        )
        self.dataframe["ind"] = self.dataframe["ind"].mask(
            cond=night_filter & self.dataframe["weekday"].isin(weekend),
            other=profile_factors["weekend"]["night"],
        )

        if self.dataframe["ind"].isnull().any(axis=0):
            logging.error("NAN value found in industrial load profile")

        time_interval = self.dataframe.index.freq.nanos / 3.6e12

        return (
            self.dataframe["ind"]
            / self.dataframe["ind"].sum()
            * annual_demand
            / time_interval
        )
