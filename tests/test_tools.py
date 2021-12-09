import datetime

import pandas as pd

from demandlib import tools


class TestWeekdays:
    @classmethod
    def setup_class(cls):
        dt_index = pd.date_range(
            datetime.datetime(2010, 1, 1, 0), periods=8760 * 4, freq="15T"
        )
        cls.df = pd.DataFrame(index=dt_index)
        cls.holidays = {
            datetime.date(2010, 1, 1): "New year",
            datetime.date(2010, 12, 25): "Christmas Day",
        }

    def test_weekdays_no_holidays(self):
        dt = tools.add_weekdays2df(self.df)
        assert dt["weekday"][0] == 5

    def test_weekdays_with_holidays(self):
        dt = tools.add_weekdays2df(self.df, holidays=self.holidays)
        assert dt["weekday"][0] == 0

    def test_weekdays_with_holidays_as_sundays(self):
        dt = tools.add_weekdays2df(
            self.df, holidays=self.holidays, holiday_is_sunday=True
        )
        assert dt["weekday"][0] == 7

    def test_christmas_with_holidays(self):
        """2010-12-25 is a Saturday, 6th day of the week."""
        dt = tools.add_weekdays2df(self.df, holidays=self.holidays)
        assert dt["weekday"][34368] == 0
        assert dt.index[34368].day == 25
