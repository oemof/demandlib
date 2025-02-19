import calendar
import os
import pandas as pd
import datetime
from demandlib.tools import add_weekdays2df
from demandlib.vdi import dwd_try
import warnings


class Region:
    def __init__(
        self, year, location, seasons=None, holidays=None, houses=None
    ):
        if calendar.isleap(year):
            self.hoy = 8784
        else:
            self.hoy = 8760
        self._datapath = os.path.join(os.path.dirname(__file__), "bdew_data")

        self._seasons = {
            "summer1": [5, 15, 9, 14],  # summer: 15.05. to 14.09
            "transition1": [3, 21, 5, 14],  # transition1 :21.03. to 14.05
            "transition2": [9, 15, 10, 31],  # transition2 :15.09. to 31.10
            "winter1": [1, 1, 3, 20],  # winter1:  01.01. to 20.03
            "winter2": [11, 1, 12, 31],  # winter2: 01.11. to 31.12
        }

        if seasons is not None:
            self._seasons.update(seasons)

        if isinstance(location, int):
            self._try_region = location
        elif isinstance(location, tuple):
            # try to create a spatial object from coordinates and find the
            # TRY region.
            raise NotImplementedError(
                "The spatial operation is not implemented, yet"
            )

        self._year = year
        self.weather = None
        self.type_days = self._get_typical_days(holidays)
        self._load_profiles = self._load_profile_factors()
        self.houses = []
        if houses is not None:
            self.add_houses(houses)

    def _get_typical_days(self, holidays):
        date_time_index = pd.date_range(
            datetime.datetime(self._year, 1, 1, 0),
            periods=self.hoy / 24,
            freq="D",
        )
        days = pd.DataFrame(index=date_time_index)
        for p in self._seasons:
            a = datetime.datetime(
                self._year, self._seasons[p][0], self._seasons[p][1], 0, 0
            )
            b = datetime.datetime(
                self._year, self._seasons[p][2], self._seasons[p][3], 23, 59
            )
            days.loc[a:b, "season"] = p[:-1]

        days = add_weekdays2df(days, holidays=holidays, holiday_is_sunday=True)
        days.pop("date")
        weatherfile = (
            "/home/uwe/git-projects/oemof/demandlib/src/demandlib/vdi/"
            "resources_weather/TRY2010_05_Jahr.dat"
        )
        self.weather = dwd_try.read_DWD_weather_file(weatherfile)
        self.weather = (
            self.weather.set_index(
                pd.date_range(
                    datetime.datetime(self._year, 1, 1, 0),
                    periods=self.hoy,
                    freq="H",
                )
            )
            .resample("D")
            .mean()
        )
        days = pd.concat([days, self.weather["CCOVER"]], axis=1)

        seasons_dict = {
            "summer": "S",
            "winter": "W",
            "transition": "U",
        }
        days.replace(to_replace=seasons_dict, inplace=True)
        days.loc[days["weekday"] == 7, "day_of_week"] = "S"
        days.loc[days["weekday"] < 7, "day_of_week"] = "W"
        days.pop("weekday")
        days.loc[days["CCOVER"] >= 5, "cloud_coverage"] = "B"
        days.loc[days["CCOVER"] < 5, "cloud_coverage"] = "H"
        days.loc[days["season"] == "S", "cloud_coverage"] = "X"
        days.pop("CCOVER")

        days["day_types"] = (
            days["season"] + days["day_of_week"] + days["cloud_coverage"]
        )

        days.drop(
            ["season", "day_of_week", "cloud_coverage"], axis=1, inplace=True
        )
        return days

    def _load_profile_factors(self):
        """Run VDI 4655 - Step 2.

        Match 'typtag' keys and reference load profile factors for each
        timestep (for each 'typtag' key, one load profile is defined by
        VDI 4655)
        """

        # Load data of typical days from VDI
        fn_typtage = os.path.join(
            os.path.dirname(__file__), "vdi_data", "VDI_4655_Typtage.csv"
        )
        typtage_df = pd.read_csv(fn_typtage, index_col=[0, 1])

        # Extract list of house types (expect: EFH, MFH)
        house_types = list(typtage_df.index.get_level_values(0).unique())

        # Convert time into datetime format
        typtage_df["time"] = pd.to_datetime(
            typtage_df.pop("Zeit"), format="%H:%M:%S"
        )

        # Calculate minutes of the day for every time step
        typtage_df["minute_of_day"] = (
            pd.to_timedelta(
                typtage_df["time"]
                - pd.Series(index=typtage_df.index, data=typtage_df["time"][0])
            )
            .dt.total_seconds()
            .div(60)
            .astype(int)
        )

        # Add columns to merge with (house types and day_types)
        typtage_df["ht"] = typtage_df.index.get_level_values(0)
        typtage_df["day_types"] = typtage_df.index.get_level_values(1)

        # Create a table for every minute of the year
        minute_table = pd.DataFrame(
            index=pd.date_range(
                f"1/1/{self._year}", periods=525600, freq="Min"
            )
        )

        # Set reference time (first hour of the day) to calculate minutes of
        # the day.
        self.type_days["ref_dt"] = self.type_days.index

        # Fill data into the large table with minute index
        self.type_days = pd.concat(
            [self.type_days, minute_table], axis=1
        ).ffill()

        # Add columns to merge with (house types, minute of day and day_types)
        self.type_days["datetime"] = self.type_days.index
        self.type_days["minute_of_day"] = (
            pd.to_timedelta(
                self.type_days.pop("datetime")
                - pd.Series(
                    index=self.type_days.index,
                    data=self.type_days.pop("ref_dt"),
                )
            )
            .dt.total_seconds()
            .div(60)
            .astype(int)
        )

        # Merge table for both house type to get the value of every minute of
        # the typical days for every minute of the year.
        house_profiles = {}
        for house_type in house_types:
            self.type_days["ht"] = "EFH"
            house_profiles[house_type] = self.type_days.merge(
                typtage_df,
                how="left",
                left_on=["day_types", "minute_of_day", "ht"],
                right_on=["day_types", "minute_of_day", "ht"],
            ).sort_index()

        # Combine the table of both house type
        load_profile = (
            pd.concat(
                [
                    house_profiles["EFH"][
                        ["F_el_n_TT", "F_Heiz_n_TT", "F_TWW_n_TT"]
                    ],
                    house_profiles["MFH"][
                        ["F_el_n_TT", "F_Heiz_n_TT", "F_TWW_n_TT"]
                    ],
                ],
                keys=["EFH", "MFH"],
                axis=1,
            )
            .swaplevel(0, 1, axis=1)
            .sort_index(axis=1)
        )

        # Set time index to make it possible to reshape the table
        load_profile = load_profile.set_index(minute_table.index)
        load_profile.ffill(inplace=True)
        load_profile.loc[:, (slice(None), "MFH",)] *= (
            1 / 15
        )
        return load_profile

    def add_houses(self, houses):
        for h in houses:
            if h["house_type"] not in ["EFH", "MFH"]:
                msg = (
                    "<{0}> is a not supported house type and will be "
                    "removed."
                )
                warnings.warn(msg.format(h["house_type"]), UserWarning)
                houses.remove(h)
        if len(houses) > 0:
            self.houses.extend(houses)

    def get_daily_energy_demand_houses(self):
        """Determine the houses' energy demand values for each 'typtag'.

        .. note::
            "The factors ``F_el_TT`` and ``F_TWW_TT`` are negative in some
            cases as they represent a variation from a one-year average. The
            values for the daily demand for electrical energy, ``W_TT``, and
            DHW energy, ``Q_TWW_TT``, usually remain positive. It is only in
            individual cases that the calculation for the typical-day category
            ``SWX`` can yield a negative value of the DHW demand. In that case,
            assume ``F_TWW_SWX`` = 0." (VDI 4655, page 16)

            This occurs when ``N_Pers`` or ``N_WE`` are too large.

        """
        # typtage_combinations = settings["typtage_combinations"]
        # houses_list = settings["houses_list_VDI"]

        # Load the file containing the energy factors of the different typical
        # radiation year (TRY) regions, house types and 'typtage'. In VDI 4655,
        # these are the tables 10 to 24.
        fn_energy_factors = os.path.join(
            os.path.dirname(__file__),
            "vdi_data",
            "VDI_4655_Typtag-Faktoren.csv",
        )
        energy_factors = pd.read_csv(
            fn_energy_factors,
            index_col=[0, 1, 2],
        )

        # if settings.get("zero_summer_heat_demand", None) is not None:
        #     # Reduze the value of 'F_Heiz_TT' to zero.
        #     # For modern houses, this eliminates the heat demand in summer
        #     energy_factors_df.loc[
        #         (slice(None), slice(None), "F_Heiz_TT"), ("SWX", "SSX")
        #     ] = 0

        # Create a new DataFrame with multiindex.
        # It has two levels of columns: houses and energy
        # The DataFrame stores the individual energy demands for each house in
        # each time step
        energy_demands_types = ["Q_Heiz_TT", "W_TT", "Q_TWW_TT"]
        house_names = [n["name"] for n in self.houses]
        iterables = [house_names, energy_demands_types]
        multiindex = pd.MultiIndex.from_product(
            iterables, names=["house", "energy"]
        )
        typtage_combinations = self.type_days["day_types"].unique()

        daily_energy_demand_houses = pd.DataFrame(
            index=multiindex, columns=typtage_combinations
        )

        # Fill the DataFrame daily_energy_demand_houses
        for house in self.houses:
            house_type = house["house_type"]
            n_pers = house["N_Pers"]
            n_we = house["N_WE"]
            try_region = self._try_region

            # Savety check:
            if try_region not in energy_factors.index.get_level_values(0):
                msg = (
                    "Error! TRY "
                    + str(try_region)
                    + " not contained in file "
                    + fn_energy_factors
                )
                msg2 = '       Skipping house "' + house["name"] + '"!'
                warnings.warn(msg + "/n" + msg2, UserWarning)
                continue  # 'Continue' skips the rest of the current for-loop

            # Get yearly energy demands
            q_heiz_a = house["Q_Heiz_a"]
            w_a = house["W_a"]
            q_tww_a = house["Q_TWW_a"]

            # (6.4) Do calculations according to VDI 4655 for each 'typtag'
            for typtag in typtage_combinations:
                f_heiz_tt = energy_factors.loc[
                    try_region, house_type, "F_Heiz_TT"
                ][typtag]
                f_el_tt = energy_factors.loc[
                    try_region, house_type, "F_el_TT"
                ][typtag]
                f_tww_tt = energy_factors.loc[
                    try_region, house_type, "F_TWW_TT"
                ][typtag]

                q_heiz_tt = q_heiz_a * f_heiz_tt

                if house_type == "EFH":
                    n_pers_we = n_pers
                elif house_type == "MFH":
                    n_pers_we = n_we
                else:
                    n_pers_we = None

                w_tt = w_a * (1.0 / 365.0 + n_pers_we * f_el_tt)
                q_tww_tt = q_tww_a * (1.0 / 365.0 + n_pers_we * f_tww_tt)

                # ToDo Add real warning.
                if w_tt < 0:
                    msg = (
                        "Warning:     W_TT for "
                        + house["name"]
                        + " and "
                        + typtag
                        + " was negative, see VDI 4655 page 16"
                    )
                    warnings.warn(msg, UserWarning)
                    w_tt = w_a * (1.0 / 365.0 + n_pers_we * 0)

                if q_tww_tt < 0:
                    msg = (
                        "Warning: Q_TWW_TT for "
                        + house["name"]
                        + " and "
                        + typtag
                        + " was negative, see VDI 4655 page 16"
                    )
                    warnings.warn(msg, UserWarning)
                    q_tww_tt = q_tww_a * (1.0 / 365.0 + n_pers_we * 0)

                # Write values into DataFrame
                daily_energy_demand_houses.loc[house["name"], "Q_Heiz_TT"][
                    typtag
                ] = q_heiz_tt
                daily_energy_demand_houses.loc[house["name"], "W_TT"][
                    typtag
                ] = w_tt
                daily_energy_demand_houses.loc[house["name"], "Q_TWW_TT"][
                    typtag
                ] = q_tww_tt

            #    print(daily_energy_demand_houses)
        return daily_energy_demand_houses

    def get_load_curve_houses(self):
        """Generate the houses' energy demand values for each timestep.

        Get the energy demand values for all days.

        This functions works through the lists houses_list and energy_factor_types
        day by day and multiplies the current load profile
        value with the daily energy demand. It returns the result: the energy
        demand values for all houses and energy types (in kWh)
        """
        daily_energy_demand_houses = self.get_daily_energy_demand_houses()

        df_typ = self.type_days.merge(
            daily_energy_demand_houses.T, left_on="day_types", right_index=True
        )
        df_typ.drop(["day_types", "minute_of_day", "ht"], axis=1, inplace=True)

        df_typ.columns = pd.MultiIndex.from_tuples(df_typ.columns)
        df_typ = df_typ.swaplevel(0, 1, axis=1).sort_index(axis=1)
        mytime = pd.DataFrame(index=self._load_profiles.index)

        load_profile_df = self._load_profiles.rename(
            columns={
                "F_Heiz_n_TT": "Q_Heiz_TT",
                "F_el_n_TT": "W_TT",
                "F_TWW_n_TT": "Q_TWW_TT",
            }
        )

        df = pd.concat([df_typ, mytime], axis=1).ffill()
        df.drop(df.head(1).index, inplace=True)

        load_curve_houses = df[load_profile_df.columns].mul(load_profile_df)

        # For each time step, each house and each type of energy factor, we
        # multiply the energy factor with the daily energy demand. The result
        # is the energy demand of that time interval.
        # We save it to the load_curve_houses DataFrame.
        # total = float(len(weather_data.index))
        # for j, date_obj in enumerate(weather_data.index):
        # helper_function(date_obj)

        # print ('{:5.1f}% done'.format(j/total*100), end='\r')  # progress

        # The typical day calculation inherently does not add up to the
        # desired total energy demand of the full year. Here we fix that:
        houses_dict = {h["name"]: h for h in self.houses}
        for column in load_curve_houses.columns:
            if column[0] == "Q_Heiz_TT":
                q_a = houses_dict[column[1]]["Q_Heiz_a"]
            elif column[0] == "Q_TWW_TT":
                q_a = houses_dict[column[1]]["Q_TWW_a"]
            elif column[0] == "W_TT":
                q_a = houses_dict[column[1]]["W_a"]
            else:
                q_a = None
            sum_ = load_curve_houses[column].sum()
            if sum_ != 0:  # Would produce NaN otherwise
                load_curve_houses[column] = (
                    load_curve_houses[column] / sum_ * q_a
                )

        return load_curve_houses


my_holidays = {
    datetime.date(2021, 5, 24): "Whit Monday",
    datetime.date(2021, 4, 5): "Easter Monday",
    datetime.date(2021, 5, 13): "Ascension Thursday",
    datetime.date(2021, 1, 1): "New year",
    datetime.date(2021, 10, 3): "Day of German Unity",
    datetime.date(2021, 12, 25): "Christmas Day",
    datetime.date(2021, 5, 1): "Labour Day",
    datetime.date(2021, 4, 2): "Good Friday",
    datetime.date(2021, 12, 26): "Second Christmas Day",
}
my_houses = [
    {
        "N_Pers": 0,
        "name": "Büro",
        "N_WE": 0,
        "Q_Heiz_a": 50000,
        "Q_Kalt_a": 7000,
        "Q_TWW_a": 1500,
        "W_a": 60000,
        "copies": 4,
        "house_type": "G1G",
        "sigma": 1,
    },
    {
        "N_Pers": 3,
        "name": "EFH",
        "N_WE": 1,
        "Q_Heiz_a": 6000,
        "TRY": 4,
        "copies": 24,
        "house_type": "EFH",
        "sigma": 4,
        'Q_TWW_a': 1500,
        'W_a': 5250,
    },
    {
        "N_Pers": 0,
        "name": "Handel",
        "N_WE": 0,
        "Q_Heiz_a": 100000,
        "Q_Kalt_a": 43000,
        "Q_TWW_a": 4500,
        "W_a": 110000,
        "copies": 9,
        "house_type": "G4G",
        "sigma": 1,
    },
    {
        "N_Pers": 45,
        "name": "MFH",
        "N_WE": 15,
        "Q_Heiz_a": 60000,
        "TRY": 4,
        "copies": 24,
        "house_type": "MFH",
        "sigma": 2,
        'Q_TWW_a': 15000,
        'W_a': 45000,
    },
]
start = datetime.datetime.now()
my_region = Region(2021, holidays=my_holidays, location=4)
my_region.add_houses(my_houses)
lc = my_region.get_load_curve_houses()
print(datetime.datetime.now() - start)

from matplotlib import pyplot as plt
lc.resample("H").sum().plot()
plt.show()
