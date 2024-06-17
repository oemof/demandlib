================
Further Profiles
================

We implemented further profiles (one until now) to represent further demand sectors which are not covered by the BDEW load profiles.
The weekdays, weekends and holidays of the year are scaled with factors to represent the demand of the respective sector.

Industrial Electrical Profile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Description
+++++++++++

The industrial electrical profile uses a step function, which is scaled with a factor to represent the demand of the industrial sector.
Day and night are separated by the am and pm function arguments. 

Usage
+++++

The industrial profile is explained in the example `electricity_demand_example.py`
located in the example folder of the repository.

.. code-block:: python

    import datetime

    import demandlib.particular_profiles as profiles
    import pandas as pd

    holidays = {
    datetime.date(2018, 1, 1): "New year",
    }

    # Add the slp for the industrial group
    ilp = profiles.IndustrialLoadProfile(
        dt_index=pd.date_range("01-01-2018", "01-01-2019", freq="15min"),
        holidays=holidays)

    # Set beginning of workday to 9 am
    ind_elec_demand = ilp.simple_profile(
        annual_demand=1e4,
        am=datetime.time(9, 0, 0),
        profile_factors={
            "week": {"day": 1.0, "night": 0.8},
            "weekend": {"day": 0.8, "night": 0.6},
            "holiday": {"day": 0.2, "night": 0.2},
        },
    )
