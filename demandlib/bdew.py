# -*- coding: utf-8 -*-
"""
Implementation of the bdew heat load profiles


"""
from math import ceil
import numpy as np
import pandas as pd
import os
from .tools import add_weekdays2df
import calendar


class ElecSlp:
    """Generate electrical standardized load profiles based on the BDEW method.

    Attributes
    ----------
    datapath : string
        Path to the csv files containing the load profile data.
    date_time_index : pandas.DateTimeIndex
        Time range for and frequency for the profile.

    Parameters
    ----------
    year : integer
        Year of the demand series.

    Optional Parameters
    -------------------
    seasons : dictionary
        Describing the time ranges for summer, winter and transition periods.
    holidays : dictionary or list
        The keys of the dictionary or the items of the list should be datetime
        objects of the days that are holidays.
    """

    def __init__(self, year, seasons=None, holidays=None):
        if calendar.isleap(year):
            hoy = 8784
        else:
            hoy = 8760
        self.datapath = os.path.join(os.path.dirname(__file__), 'bdew_data')
        self.date_time_index = pd.date_range(
            pd.datetime(year, 1, 1, 0), periods=hoy * 4, freq='15Min')
        if seasons is None:
            self.seasons = {
                'summer1': [5, 15, 9, 14],  # summer: 15.05. to 14.09
                'transition1': [3, 21, 5, 14],  # transition1 :21.03. to 14.05
                'transition2': [9, 15, 10, 31],  # transition2 :15.09. to 31.10
                'winter1': [1, 1, 3, 20],  # winter1:  01.01. to 20.03
                'winter2': [11, 1, 12, 31],  # winter2: 01.11. to 31.12
            }
        else:
            self.seasons = seasons
        self.year = year
        self.slp_frame = self.all_load_profiles(self.date_time_index,
                                                holidays=holidays)

    def all_load_profiles(self, time_df, holidays=None):
        slp_types = ['h0', 'g0', 'g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'l0',
                     'l1', 'l2']
        new_df = self.create_bdew_load_profiles(time_df, slp_types,
                                                holidays=holidays)

        new_df.drop(['hour', 'weekday'], 1, inplace=True)
        return new_df

    def create_bdew_load_profiles(self, dt_index, slp_types, holidays=None):
        """Calculates the hourly electricity load profile in MWh/h of a region.
        """

        # define file path of slp csv data
        file_path = os.path.join(self.datapath, 'selp_series.csv')

        # Read standard load profile series from csv file
        selp_series = pd.read_csv(file_path)
        tmp_df = selp_series
        # Create an index to merge. The year and month will be ignored only the
        # time index is necessary.
        index = pd.date_range(
            pd.datetime(2007, 1, 1, 0), periods=2016, freq='15Min')
        tmp_df.set_index(index, inplace=True)

        # Create empty DataFrame to take the results.
        new_df = pd.DataFrame(index=dt_index, columns=slp_types).fillna(0)
        new_df = add_weekdays2df(new_df, holidays=holidays,
                                 holiday_is_sunday=True)

        new_df['hour'] = dt_index.hour + 1
        new_df['minute'] = dt_index.minute
        time_df = new_df[['date', 'hour', 'minute', 'weekday']].copy()
        tmp_df[slp_types] = tmp_df[slp_types].astype(float)

        # Inner join the slps on the time_df to the slp's for a whole year
        tmp_df['hour_of_day'] = tmp_df.index.hour + 1
        tmp_df['minute_of_hour'] = tmp_df.index.minute
        left_cols = ['hour_of_day', 'minute_of_hour', 'weekday']
        right_cols = ['hour', 'minute', 'weekday']
        tmp_df = tmp_df.reset_index()
        tmp_df.pop('index')

        for p in self.seasons.keys():
            a = pd.datetime(self.year, self.seasons[p][0],
                            self.seasons[p][1], 0, 0)
            b = pd.datetime(self.year, self.seasons[p][2],
                            self.seasons[p][3], 23, 59)
            new_df.update(pd.DataFrame.merge(
                tmp_df[tmp_df['period'] == p[:-1]], time_df[a:b],
                left_on=left_cols, right_on=right_cols,
                how='inner', left_index=True).sort_index().drop(
                ['hour_of_day'], 1))

        new_df.drop('date', axis=1, inplace=True)
        return new_df.div(new_df.sum(axis=0), axis=1)

    def get_profile(self, ann_el_demand_per_sector):
        """ Get the profiles for the given annual demand

        Parameters
        ----------
        ann_el_demand_per_sector : dictionary
            Key: sector, value: annual value

        Returns
        -------
        pandas.DataFrame : Table with all profiles

        """
        return self.slp_frame.multiply(pd.Series(
            ann_el_demand_per_sector), axis=1).dropna(how='all', axis=1) * 4


class HeatBuilding:
    """
    Parameters
    ----------
    year : int
        year for which the profile is created

    Attributes
    ----------
    datapath : string
        path to the bdew basic data files (csv)
    temperature : pandas.Series
        Series containing hourly temperature data
    annual_heat_demand : float
        annual heat demand of building in kWh
    building_class: int
        class of building according to bdew classification
        possible numbers are: 1 - 11
    shlp_type : string
        type of standardized heat load profile according to bdew
        possible types are:
        GMF, GPD, GHD, GWA, GGB, EFH, GKO, MFH, GBD, GBA, GMK, GBH, GGA, GHA
    wind_class : int
        wind classification for building location (0=not windy or 1=windy)
    ww_incl : boolean
        decider whether warm water load is included in the heat load profile
    """

    def __init__(self, df_index, **kwargs):
        self.datapath = kwargs.get(
            'datapath', os.path.join(os.path.dirname(__file__), 'bdew_data'))
        self.df = pd.DataFrame(index=df_index)
        self.df = add_weekdays2df(self.df, holiday_is_sunday=True,
                                  holidays=kwargs.get('holidays'))
        self.df['hour'] = self.df.index.hour + 1
        self.temperature = kwargs.get('temperature')
        self.annual_heat_demand = kwargs.get('annual_heat_demand')
        self.shlp_type = kwargs.get('shlp_type').upper()
        self.wind_class = kwargs.get('wind_class')
        self.building_class = kwargs.get('building_class', 0)
        self.ww_incl = kwargs.get('ww_incl', True)
        self.name = kwargs.get('name', self.shlp_type)

    def weighted_temperature(self, how='geometric_series'):
        r"""
        A new temperature vector is generated containing a multi-day
        average temperature as needed in the load profile function.

        Parameters
        ----------
        how : string
            string which type to return ("geometric_series" or "mean")

        Notes
        -----
        Equation for the mathematical series of the average
        tempaerature [1]_:

        .. math::
            T=\frac{T_{D}+0.5\cdot T_{D-1}+0.25\cdot T_{D-2}+
                    0.125\cdot T_{D-3}}{1+0.5+0.25+0.125}

        with :math:`T_D` = Average temperature on the present day
             :math:`T_{D-i}` = Average temperature on the day - i

        References
        ----------
        .. [1] `BDEW <https://www.avacon.de/cps/rde/xbcr/avacon/15-06-30_Leitfaden_Abwicklung_SLP_Gas.pdf>`_,
            BDEW Documentation for heat profiles.
        """

        # calculate daily mean temperature
        temperature = self.df['temperature'].resample('D').mean().reindex(
            self.df.index).fillna(method='ffill').fillna(method='bfill')

        if how == 'geometric_series':
            temperature_mean = (temperature + 0.5 * np.roll(temperature, 24) +
                                0.25 * np.roll(temperature, 48) +
                                0.125 * np.roll(temperature, 72)) / 1.875
        elif how == 'mean':
            temperature_mean = temperature
        else:
            temperature_mean = None

        return temperature_mean

    def get_temperature_interval(self):
        """Appoints the corresponding temperature interval to each temperature
        in the temperature vector.
        """
        intervals = ({
            -20: 1, -19: 1, -18: 1, -17: 1, -16: 1, -15: 1, -14: 2,
            -13: 2, -12: 2, -11: 2, -10: 2, -9: 3, -8: 3, -7: 3, -6: 3, -5: 3,
            -4: 4, -3: 4, -2: 4, -1: 4, 0: 4, 1: 5, 2: 5, 3: 5, 4: 5, 5: 5,
            6: 6, 7: 6, 8: 6, 9: 6, 10: 6, 11: 7, 12: 7, 13: 7, 14: 7, 15: 7,
            16: 8, 17: 8, 18: 8, 19: 8, 20: 8, 21: 9, 22: 9, 23: 9, 24: 9,
            25: 9, 26: 10, 27: 10, 28: 10, 29: 10, 30: 10, 31: 10, 32: 10,
            33: 10, 34: 10, 35: 10, 36: 10, 37: 10, 38: 10, 39: 10, 40: 10})

        temperature_rounded = [ceil(i) for i in self.df['temperature_geo']]

        temperature_interval = [intervals[i] for i in temperature_rounded]

        return np.transpose(np.array(temperature_interval))

    def get_sf_values(self, filename='shlp_hour_factors.csv'):
        """ Determine the h-values

        Parameters
        ----------
        filename : string
            name of file where sigmoid factors are stored
        """
        file = os.path.join(self.datapath, filename)
        hour_factors = pd.read_csv(file, index_col=0)
        hour_factors = hour_factors.query(
            'building_class=={0} and shlp_type=="{1}"'.format(
                self.building_class, self.shlp_type))

        # Join the two DataFrames on the columns 'hour' and 'hour_of_the_day'
        # or ['hour' 'weekday'] and ['hour_of_the_day', 'weekday'] if it is
        # not a residential slp.
        residential = self.building_class > 0
        left_cols = ['hour_of_day'] + (['weekday'] if not residential else [])
        right_cols = ['hour'] + (['weekday'] if not residential else [])
        sf_mat = pd.DataFrame.merge(
            hour_factors, self.df, left_on=left_cols, right_on=right_cols,
            how='outer', left_index=True).sort_index()

        # drop unnecessary columns
        drop_cols = (
            ['hour_of_day', 'hour', 'building_class', 'shlp_type',
             'date', 'temperature'] + (['weekday_x'] if residential else []) +
            (['weekday_y'] if residential else []) +
            (['weekday'] if not residential else []))
        sf_mat = sf_mat.drop(drop_cols, 1)

        # Determine the h values
        length = len(self.temperature)
        sf = (np.array(sf_mat)[np.array(list(range(0, length)))[:],
                               (self.get_temperature_interval() - 1)[:]])
        return np.array(list(map(float, sf[:])))

    def get_sigmoid_parameters(self, filename='shlp_sigmoid_factors.csv'):
        """ Retrieve the sigmoid parameters from csv-files

        Parameters
        ----------
        filename : string
            name of file where sigmoid factors are stored
        """

        file = os.path.join(self.datapath, filename)
        sigmoid = pd.read_csv(file, index_col=0)
        sigmoid = sigmoid.query(
            'building_class=={0} and '.format(self.building_class) +
            'shlp_type=="{0}" and '.format(self.shlp_type) +
            'wind_impact=={0}'.format(self.wind_class))

        a = float(sigmoid['parameter_a'])
        b = float(sigmoid['parameter_b'])
        c = float(sigmoid['parameter_c'])
        if self.ww_incl:
            d = float(sigmoid['parameter_d'])
        else:
            d = 0
        return a, b, c, d

    def get_weekday_parameters(self, filename='shlp_weekday_factors.csv'):
        """ Retrieve the weekday parameter from csv-file

        Parameters
        ----------
        filename : string
            name of file where sigmoid factors are stored
        """
        file = os.path.join(self.datapath, filename)
        f_df = pd.read_csv(file, index_col=0)

        tmp_df = f_df.query('shlp_type=="{0}"'.format(self.shlp_type)).drop(
            'shlp_type', axis=1)

        tmp_df['weekdays'] = np.array(list(range(7))) + 1

        return np.array(list(map(float, pd.DataFrame.merge(
            tmp_df, self.df, left_on='weekdays', right_on='weekday',
            how='inner', left_index=True).sort_index()['wochentagsfaktor'])))

    def get_bdew_profile(self):
        """ Calculation of the hourly heat demand using the bdew-equations
        """
        return self.get_normalized_bdew_profile() * self.annual_heat_demand

    def get_normalized_bdew_profile(self):
        """ Calculation of the normalized hourly heat demand
        """
        self.df['temperature'] = self.temperature.values
        self.df['temperature_geo'] = self.weighted_temperature(
            how='geometric_series')

        sf = self.get_sf_values()

        [a, b, c, d] = self.get_sigmoid_parameters()

        f = self.get_weekday_parameters()
        h = (a / (1 + (b / (self.df['temperature_geo'] - 40)) ** c) + d)
        kw = 1.0 / (sum(h * f) / 24)
        heat_profile_normalized = (kw * h * f * sf)

        return heat_profile_normalized

    def cop(self, heatpump_type = "Air", water_temp = 60):
        """ Calculation of the coefficient of performance depending
        on the outside temperature
        
        Parameters
        ----------
        heatpump_type: string
            defines the technology used. Ground is more efficient than Air.
        water_temp: int
            temperature needed for the heating system
            
        References
        ----------
        ..  [1]: 'https://www.researchgate.net/publication/255759857_A_review_of_domestic_heat_pumps'
            Research paper about domestic heatpumps, containing the formulas used
        """
        mean_temp_hours = pd.DataFrame(self.temperature)
        cop_lst = []
        
        if heatpump_type == "Air":
            for i, tmp in mean_temp_hours.iterrows():
                cop = (6.81 - 0.121 * (water_temp - tmp)
                       + 0.00063 * (water_temp - tmp)**2)
                cop_lst.append(cop)
        
        elif heatpump_type == "Ground":
            for i, tmp in mean_temp_hours.iterrows():
                cop = (8.77 - 0.15 * (water_temp - tmp)
                       + 0.000734 * (water_temp - tmp)**2)
                cop_lst.append(cop)
        
        else:
            print("Heatpump type is not defined")
            return -9999
    
#        df_cop = pd.DataFrame({'cop': cop_lst}) #change column name of list to 'cop'
        df_cop = pd.DataFrame(cop_lst)
        return df_cop
    
    