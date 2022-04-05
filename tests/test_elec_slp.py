import datetime

import pandas as pd
import pytest

from demandlib import bdew


class TestElecSLP:
    @classmethod
    def setup_class(cls):
        cls.slp = bdew.ElecSlp(2010)
        cls.dt_index = pd.date_range(
            datetime.datetime(2010, 1, 1, 0), periods=8760 * 4, freq="15Min"
        )
        cls.slp_types = [
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
        cls.holidays = {
            datetime.date(2010, 5, 24): "Whit Monday",
            datetime.date(2010, 4, 5): "Easter Monday",
            datetime.date(2010, 5, 13): "Ascension Thursday",
            datetime.date(2010, 1, 1): "New year",
            datetime.date(2010, 10, 3): "Day of German Unity",
            datetime.date(2010, 12, 25): "Christmas Day",
            datetime.date(2010, 5, 1): "Labour Day",
            datetime.date(2010, 4, 2): "Good Friday",
            datetime.date(2010, 12, 26): "Second Christmas Day",
        }

    def test_elec_slp_year(self):
        assert self.slp._year == 2010

    def test_columns_of_frame(self):
        assert sorted(self.slp.slp_frame.columns) == [
            "g0",
            "g1",
            "g2",
            "g3",
            "g4",
            "g5",
            "g6",
            "h0",
            "h0_dyn",
            "l0",
            "l1",
            "l2",
        ]

    def test_index_of_frame(self):
        assert isinstance(self.slp.slp_frame.index, pd.DatetimeIndex)
        assert len(self.slp.slp_frame.index) == 8760 * 4

    def test_index_for_leap_year(self):
        assert len(bdew.ElecSlp(2012).slp_frame.index) == 8760 * 4 + 24 * 4

    def test_frame_without_holidays(self):
        my_frame = self.slp.create_bdew_load_profiles(
            self.dt_index, self.slp_types, holidays=None
        )
        my_frame = pd.concat(
            [my_frame, self.slp.create_dynamic_h0_profile()], axis=1
        )
        pd.testing.assert_frame_equal(self.slp.slp_frame, my_frame)

    def test_frame_with_holidays(self):
        my_frame = self.slp.create_bdew_load_profiles(
            self.dt_index, self.slp_types, holidays=self.holidays
        )
        with pytest.raises(AssertionError):
            pd.testing.assert_frame_equal(self.slp.slp_frame, my_frame)

        # with holidays
        assert (
            round(my_frame.loc[datetime.datetime(2010, 5, 24, 12, 0), "h0"], 6)
            == 0.000054
        )
        # without holidays
        assert (
            round(
                self.slp.slp_frame.loc[
                    datetime.datetime(2010, 5, 24, 12, 0), "h0"
                ],
                6,
            )
            == 0.000038
        )

    def test_deprecated_method(self):
        with pytest.warns(FutureWarning) as record:
            self.slp.get_profile(ann_el_demand_per_sector={"h0": 5000})
        assert len(record) == 1
        assert "This method is deprecated" in record[0].message.args[0]


def test_changed_seasons():
    """Test changing the seasons."""
    alt_seasons = {
        "summer1": [5, 2, 9, 14],  # summer: 2.05. to 14.09
        "transition1": [3, 21, 5, 1],  # transition1 :21.03. to 1.05.
    }
    slp1 = bdew.ElecSlp(2010)
    slp2 = bdew.ElecSlp(2010, seasons=alt_seasons)
    # 6th-7th May, 2010
    assert slp1.get_profiles("g0").index[12000] == datetime.datetime(
        2010, 5, 6, 0, 0
    )
    assert slp1.get_profiles("g0").index[12096] == datetime.datetime(
        2010, 5, 7, 0, 0
    )
    # transition1 in a normal slp
    assert (
        round(float(slp1.get_profiles("g0").iloc[12000:12096].sum()), 5)
        == 0.00300
    )
    # summer1 in a changed time scale
    assert (
        round(float(slp2.get_profiles("g0").iloc[12000:12096].sum()), 5)
        == 0.00289
    )
