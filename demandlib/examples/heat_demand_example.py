# -*- coding: utf-8 -*-
"""
Creating heat demand profiles using the bdew method.

Installation requirements
-------------------------
This example requires at least version v0.1.4 of the oemof demandlib. Install
by:
    pip install 'demandlib>=0.1.4,<0.2'
Optional:
    pip install matplotlib

"""

import pandas as pd
import demandlib.bdew as bdew
import datetime
import os
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

# read example temperature series

datapath = os.path.join(os.path.dirname(__file__), 'example_data.csv')
temperature = pd.read_csv(datapath)["temperature"]


# The following dictionary is create by "workalendar"
# pip3 install workalendar
# >>> from workalendar.europe import Germany
# >>> cal = Germany()
# >>> holidays = dict(cal.holidays(2010))


def heat_example():
    holidays = {
        datetime.date(2010, 5, 24): 'Whit Monday',
        datetime.date(2010, 4, 5): 'Easter Monday',
        datetime.date(2010, 5, 13): 'Ascension Thursday',
        datetime.date(2010, 1, 1): 'New year',
        datetime.date(2010, 10, 3): 'Day of German Unity',
        datetime.date(2010, 12, 25): 'Christmas Day',
        datetime.date(2010, 5, 1): 'Labour Day',
        datetime.date(2010, 4, 2): 'Good Friday',
        datetime.date(2010, 12, 26): 'Second Christmas Day'}

    # Create DataFrame for 2010
    demand = pd.DataFrame(
        index=pd.date_range(pd.datetime(2010, 1, 1, 0),
                            periods=8760, freq='H'))
    
    # Single family house (efh: Einfamilienhaus)
    demand['efh'] = bdew.HeatBuilding(
        demand.index, holidays=holidays, temperature=temperature,
        shlp_type='EFH',
        building_class=1, wind_class=1, annual_heat_demand=25000,
        name='EFH').get_bdew_profile()

    # Multi family house (mfh: Mehrfamilienhaus)
    demand['mfh'] = bdew.HeatBuilding(
        demand.index, holidays=holidays, temperature=temperature,
        shlp_type='MFH',
        building_class=2, wind_class=0, annual_heat_demand=80000,
        name='MFH').get_bdew_profile()

    # Industry, trade, service (ghd: Gewerbe, Handel, Dienstleistung)
    demand['ghd'] = bdew.HeatBuilding(
        demand.index, holidays=holidays, temperature=temperature,
        shlp_type='ghd', wind_class=0, annual_heat_demand=140000,
        name='ghd').get_bdew_profile()

    if plt is not None:
        # Plot demand of building
        ax = demand.plot()
        ax.set_xlabel("Date")
        ax.set_ylabel("Heat demand in kW")
        plt.show()
    else:
        print('Annual consumption: \n{}'.format(demand.sum()))


if __name__ == '__main__':
    heat_example()
