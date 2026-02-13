# -*- coding: utf-8 -*-
"""
Implementation of industrial step load profiles.


"""
from datetime import time as settime

import pandas as pd

from .tools import add_weekdays2df


class IndustrialLoadProfile:
    """Generate an industrial heat or electricity load profile."""

    def __init__(self, dt_index, holidays=None, holiday_is_sunday=False):
        """
        Initialize the industrial load profile.

        Parameters
        ----------
        dt_index : pandas.DatetimeIndex
            Datetime index for the load profile.
        holidays : dict
            Dictionary with keys of type datetime and values with holiday name
            as str, e.g. {datetime.date(2010, 1, 1): "New year"}. See the
            electricity_demand_example in the examples directory for
            information on how to obtain holidays using workalender.
            Per default, no holidays are used.
            Default: None.
        holiday_is_sunday : bool
            If True, holidays are treated as Sundays. If False, holidays are
            assigned weekday 0 and separate holiday scaling factors are applied
            in method simple_profile().
            Default: False.

        """
        self.dataframe = pd.DataFrame(index=dt_index)
        self.dataframe = add_weekdays2df(
            self.dataframe,
            holiday_is_sunday=holiday_is_sunday,
            holidays=holidays,
        )

    def simple_profile(self, annual_demand, **kwargs):
        """
        Create industrial step load profile.

        Parameters
        ----------
        annual_demand : float
            Total demand over the period given upon initialisation
            of IndustrialLoadProfile through parameter `dt_index`. This is
            actually only the annual demand, if an entire year was given.

        Other Parameters
        ----------------
        am : datetime.time
            Defines the beginning of the workday. Times between `am` and `pm`,
            including the start and end time defined by `am` and `pm`, are
            assigned "day" factors from `profile_factors`. Other times are
            assigned "night" factors.
            Default: 7 a.m.
        pm : datetime.time
            Defines the end of the workday. Times between `am` and `pm`,
            including the start and end time defined by `am` and `pm`, are
            assigned "day" factors from `profile_factors`. Other times are
            assigned "night" factors.
            Default: 11:30 p.m.
        week : list(int)
            List of weekdays, where 1 corresponds to Monday, 2 to Tuesday, etc.
            Weekdays are assigned "week" factors from `profile_factors`.
            Default: [1, 2, 3, 4, 5].
        weekend : list(int)
            List of weekend days, where 1 corresponds to Monday, 2 to Tuesday,
            etc. Weekend days are assigned "weekend" factors from
            `profile_factors`.
            Default: [6, 7].
        holiday : list(int)
            List of holiday days. Holidays given upon initialisation of the
            IndustrialLoadProfile object are tagged with weekday 0 if
            `holiday_is_sunday` is set to False, wherefore the default for this
            parameter is [0].
            Holidays are assigned "holiday" factors from `profile_factors`.
            Default: [0].
        profile_factors : dict
            Dictionary with load profile scaling factors for night and day of
            weekdays, weekend days and holidays. The dictionary must have the
            same form as the dictionary given as the default value.
            Default:

            .. code:: python

                {
                    "week": {"day": 0.8, "night": 0.6},
                    "weekend": {"day": 0.9, "night": 0.7},
                    "holiday": {"day": 0.9, "night": 0.7},
                }

        Returns
        -------
        pd.Series
            Series with demand per time step (unit depends on the unit the
            `annual_demand` was provided with). Index is a DatetimeIndex
            containing all time steps the IndustrialLoadProfile was initialised
            with.

        """

        # Define day (am to pm), night (pm to am), week day (week),
        # weekend day (weekend) and holiday
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
        # check profile factors
        for key in ["week", "weekend", "holiday"]:
            if key not in profile_factors.keys():
                raise ValueError(
                    f"Missing entry for '{key}' in profile_factors."
                )
            else:
                if "day" not in profile_factors[key].keys():
                    raise ValueError(
                        f"Missing entry for 'day' in profile_factors for "
                        f"'{key}'."
                    )
                elif "night" not in profile_factors[key].keys():
                    raise ValueError(
                        f"Missing entry for 'night' in profile_factors for "
                        f"'{key}'."
                    )

        self.dataframe["ind"] = 0.0

        day_mask = self.dataframe.index.indexer_between_time(
            am, pm, include_start=True, include_end=True
        )
        day_filter = pd.Series(False, index=self.dataframe.index)
        day_filter.iloc[day_mask] = True
        # set up night filter as the reverse of the day filter
        night_filter = pd.Series(True, index=self.dataframe.index)
        night_filter.iloc[day_mask] = False

        week_filter = self.dataframe["weekday"].isin(week)
        weekend_filter = self.dataframe["weekday"].isin(weekend)
        holiday_filter = self.dataframe["weekday"].isin(holiday)

        # Update 'ind' column based on day/night filters and
        # weekday/weekend/holiday conditions
        self.dataframe.loc[day_filter & week_filter, "ind"] = profile_factors[
            "week"
        ]["day"]
        self.dataframe.loc[night_filter & week_filter, "ind"] = (
            profile_factors["week"]["night"]
        )
        self.dataframe.loc[day_filter & weekend_filter, "ind"] = (
            profile_factors["weekend"]["day"]
        )
        self.dataframe.loc[night_filter & weekend_filter, "ind"] = (
            profile_factors["weekend"]["night"]
        )
        self.dataframe.loc[day_filter & holiday_filter, "ind"] = (
            profile_factors["holiday"]["day"]
        )
        self.dataframe.loc[night_filter & holiday_filter, "ind"] = (
            profile_factors["holiday"]["night"]
        )

        time_interval = self.dataframe.index.freq.nanos / 3.6e12

        return (
            self.dataframe["ind"]
            / self.dataframe["ind"].sum()
            * annual_demand
            / time_interval
        )
