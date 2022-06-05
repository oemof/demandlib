"""Tools needed by the main classes
"""
import pandas as pd


def add_weekdays2df(time_df, holidays=None, holiday_is_sunday=False):
    r"""Giving back a DataFrame containing weekdays and optionally holidays for
     the given year.

    Parameters
    ----------
    time_df : pandas DataFrame
        DataFrame to which the weekdays should be added

    Optional Parameters
    -------------------
    holidays : array with information for every hour of the year, if holiday or
        not (0: holiday, 1: no holiday)
    holiday_is_sunday : boolean
        If set to True, all holidays (0) will be set to sundays (7).

    Returns
    -------
    pandas.DataFrame : DataFrame with weekdays

    Notes
    -----
    Using Pandas > 0.16

    """
    time_df["weekday"] = time_df.index.weekday + 1
    time_df["date"] = time_df.index.date

    # Set weekday to Holiday (0) for all holidays
    if holidays is not None:
        if isinstance(holidays, dict):
            holidays = list(holidays.keys())
        time_df["weekday"].mask(
            pd.to_datetime(time_df["date"]).isin(pd.to_datetime(holidays)),
            0,
            True,
        )

    if holiday_is_sunday:
        time_df.weekday.mask(cond=time_df.weekday == 0, other=7, inplace=True)

    return time_df
