# -*- coding: utf-8 -*-
"""
Implementation of the bdew standard load profiles for electric power.


"""
import logging
from datetime import time as settime
import warnings

import pandas as pd

from .tools import add_weekdays2df


class IndustrialLoadProfile:
    """Generate an industrial heat or electric load profile."""

    def __init__(self, dt_index, holidays=None):
        self.dataframe = pd.DataFrame(index=dt_index)
        if holidays is not None:
            # treat holidays as independent days (value 0 is holiday)
            self.dataframe = add_weekdays2df(
                self.dataframe, holiday_is_sunday=False, holidays=holidays
            )
        else:
            # treat all holidays as sundays
            self.dataframe = add_weekdays2df(
                self.dataframe, holiday_is_sunday=True, holidays=holidays
            )

    def simple_profile(self, annual_demand, **kwargs):
        """
        Create industrial load profile

        Parameters
        ----------
        annual_demand : float
            Total annual demand.

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
            dictionary with scaling factors for night and day of weekdays,
            weekend days and holidays.
        """

        # Day(am to pm), night (pm to am), week day (week),
        # weekend day (weekend)
        am = kwargs.get("am", settime(7, 00, 0))
        pm = kwargs.get("pm", settime(23, 30, 0))

        week = kwargs.get("week", [1, 2, 3, 4, 5])
        weekend = kwargs.get("weekend", [6, 7])
        holiday = kwargs.get("holiday", [0])

        default_factors = {
            "week": {"day": 0.8, "night": 0.6},
            "weekend": {"day": 0.9, "night": 0.7},
            "holiday": {"day": 0.9, "night": 0.7},
        }

        profile_factors = kwargs.get("profile_factors", default_factors)

        self.dataframe["ind"] = 0.0

        # Apply masks to the dataframe so that the profile factors are applied
        def apply_masks(dataframe, profile_factors, am, pm, week, weekend, holiday):
            conditions = [
                {"cond": dataframe["weekday"].between_time(am, pm).isin(week),
                 "period": ("week", "day")},
                {"cond": dataframe["weekday"].between_time(pm, am).isin(week),
                 "period": ("week", "night")},
                {"cond": dataframe["weekday"].between_time(am, pm).isin(weekend),
                 "period": ("weekend", "day")},
                {"cond": dataframe["weekday"].between_time(pm, am).isin(weekend),
                 "period": ("weekend", "night")},
                {"cond": dataframe["weekday"].between_time(am, pm).isin(holiday),
                 "period": ("weekend", "day")},
                {"cond": dataframe["weekday"].between_time(pm, am).isin(holiday),
                 "period": ("weekend", "night")},
            ]

            for condition in conditions:
                try:
                    period, time_of_day = condition["period"]
                    dataframe["ind"].mask(
                        cond=condition["cond"],
                        other=profile_factors[period][time_of_day],
                        inplace=True,
                    )
                except KeyError as e:
                    warnings.warn(f"Missing entry for {e} in profile_factors", UserWarning)

        # Example usage
        apply_masks(self.dataframe, profile_factors, am, pm, week, weekend, holiday)

        if self.dataframe["ind"].isnull().any(axis=0):
            logging.error("NAN value found in industrial load profile")

        time_interval = self.dataframe.index.freq.nanos / 3.6e12

        return (
            self.dataframe["ind"]
            / self.dataframe["ind"].sum()
            * annual_demand
            / time_interval
        )
