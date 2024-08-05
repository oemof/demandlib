import datetime

import numpy as np
import pandas as pd
import pytest

from demandlib.particular_profiles import IndustrialLoadProfile


class TestIndustrialLoadProfile:
    @classmethod
    def setup_class(cls):
        dt_index = pd.date_range(
            datetime.datetime(2010, 1, 1, 0), periods=24 * 7, freq="1h"
        )
        holidays = {
            datetime.date(2010, 1, 1): "New year",
        }
        cls.ilp = IndustrialLoadProfile(
            dt_index=dt_index,
            holidays=holidays,
            holiday_is_sunday=False,
        )
        cls.ilp_holiday = IndustrialLoadProfile(
            dt_index=dt_index,
            holidays=holidays,
            holiday_is_sunday=True,
        )

    def test_simple_profile_default_values(self):
        """
        test with default values

        """
        df = self.ilp.simple_profile(1.0)

        # check factors in self.dataframe["ind"]
        # holiday
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-01 6:00"), "ind"]
            == 0.7
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-01 7:00"), "ind"]
            == 0.9
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-01 23:00"), "ind"]
            == 0.9
        )
        # weekend day
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-02 6:00"), "ind"]
            == 0.7
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-02 7:00"), "ind"]
            == 0.9
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-02 23:00"), "ind"]
            == 0.9
        )
        # week day
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-04 6:00"), "ind"]
            == 0.6
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-04 7:00"), "ind"]
            == 0.8
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-04 23:00"), "ind"]
            == 0.8
        )

        # check sum of factors to make sure not only the tested factors are
        # correct - the factors don't add up to 100 but to some number that
        # depends on the given profile factors and time steps; as long as
        # these don't change the number checked here should not change either
        assert np.isclose(self.ilp.dataframe["ind"].sum(), 131.8)
        # check total demand
        assert np.isclose(df.sum(), 1.0)

    def test_simple_profile_own_values(self):
        """
        test with own values

        """
        profile_factors = {
            "week": {"day": 0.6, "night": 0.5},
            "weekend": {"day": 0.7, "night": 0.4},
            "holiday": {"day": 0.8, "night": 0.3},
        }
        week = [2, 3, 4, 5]
        weekend = [1, 6, 7]
        df = self.ilp.simple_profile(
            1.0,
            week=week,
            weekend=weekend,
            profile_factors=profile_factors,
            am=datetime.time(6, 30, 0),
            pm=datetime.time(22, 00, 0),
        )

        # check factors in self.dataframe["ind"]
        # holiday
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-01 6:00"), "ind"]
            == 0.3
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-01 7:00"), "ind"]
            == 0.8
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-01 23:00"), "ind"]
            == 0.3
        )
        # weekend day
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-02 6:00"), "ind"]
            == 0.4
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-02 7:00"), "ind"]
            == 0.7
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-02 22:00"), "ind"]
            == 0.7
        )
        # Monday - now set to be weekend day
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-04 6:00"), "ind"]
            == 0.4
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-04 7:00"), "ind"]
            == 0.7
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-04 23:00"), "ind"]
            == 0.4
        )
        # week day
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-05 6:00"), "ind"]
            == 0.5
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-05 7:00"), "ind"]
            == 0.6
        )
        assert (
            self.ilp.dataframe.at[pd.Timestamp("2010-01-05 23:00"), "ind"]
            == 0.5
        )

        # check sum of factors to make sure not only the tested factors are
        # correct - the factors don't add up to 100 but to some number that
        # depends on the given profile factors and time steps; as long as
        # these don't change the number checked here should not change either
        assert np.isclose(self.ilp.dataframe["ind"].sum(), 99.2)
        # check total demand
        assert np.isclose(df.sum(), 1.0)

    def test_simple_profile_error_raising(self):
        """
        test error raising in case of missing profile factors

        """
        profile_factors = {
            "week": {"day": 0.6, "night": 0.5},
        }
        msg = "Missing entry for 'weekend' in profile_factors."
        with pytest.raises(ValueError, match=msg):
            self.ilp.simple_profile(
                1.0,
                profile_factors=profile_factors,
            )

        profile_factors = {
            "week": {"day": 0.6},
        }
        msg = "Missing entry for 'night' in profile_factors for 'week'."
        with pytest.raises(ValueError, match=msg):
            self.ilp.simple_profile(
                1.0,
                profile_factors=profile_factors,
            )

    def test_simple_profile_holiday_is_sunday(self):
        """
        test with default values and holiday_is_sunday = True

        """
        profile_factors = {
            "week": {"day": 0.6, "night": 0.5},
            "weekend": {"day": 0.7, "night": 0.4},
            "holiday": {"day": 0.8, "night": 0.3},
        }
        df = self.ilp_holiday.simple_profile(
            1.0, profile_factors=profile_factors
        )

        # check factors in self.dataframe["ind"]
        # holiday - now treated as Sunday
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-01 6:00"), "ind"
            ]
            == 0.4
        )
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-01 7:00"), "ind"
            ]
            == 0.7
        )
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-01 23:00"), "ind"
            ]
            == 0.7
        )
        # weekend day
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-02 6:00"), "ind"
            ]
            == 0.4
        )
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-02 7:00"), "ind"
            ]
            == 0.7
        )
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-02 23:00"), "ind"
            ]
            == 0.7
        )
        # week day
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-04 6:00"), "ind"
            ]
            == 0.5
        )
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-04 7:00"), "ind"
            ]
            == 0.6
        )
        assert (
            self.ilp_holiday.dataframe.at[
                pd.Timestamp("2010-01-04 23:00"), "ind"
            ]
            == 0.6
        )

        # check sum of factors to make sure not only the tested factors are
        # correct - the factors don't add up to 100 but to some number that
        # depends on the given profile factors and time steps; as long as
        # these don't change the number checked here should not change either
        assert np.isclose(self.ilp_holiday.dataframe["ind"].sum(), 98.9)
        # check total demand
        assert np.isclose(df.sum(), 1.0)
