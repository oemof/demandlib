================
Further Profiles
================

We implemented further profiles (one until now) to represent further demand sectors which are not covered by the BDEW load profiles.

Industrial Electrical Profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Description
+++++++++++

The industrial electrical profile uses a step function synthesized using different
scaling factors for weekdays, weekend days and holidays as well as day time and night
time.

Usage
+++++
The industrial profile is explained in the example `electricity_demand_example.py`
located in the examples directory of the repository.

.. code-block:: python
    import datetime
    import demandlib.particular_profiles as profiles
    import pandas as pd

    holidays = {
        datetime.date(2018, 1, 1): "New year",
    }
    # Set up IndustrialLoadProfile
    ilp = profiles.IndustrialLoadProfile(
        dt_index=pd.date_range("01-01-2018", "01-01-2019", freq="15min"),
        holidays=holidays
    )
    # Get step load profile with own scaling factors and definition of
    # beginning of workday
    ind_elec_demand = ilp.simple_profile(
        annual_demand=1e4,
        am=datetime.time(9, 0, 0),
        profile_factors={
            "week": {"day": 1.0, "night": 0.8},
            "weekend": {"day": 0.8, "night": 0.6},
            "holiday": {"day": 0.2, "night": 0.2},
        },
    )
