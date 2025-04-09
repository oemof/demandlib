"""
Tests for the VDI 4655 regions module.

SPDX-License-Identifier: MIT
"""

import datetime
import os
import sys
from pathlib import Path

import pandas as pd
import pytest

import demandlib.vdi
from demandlib.vdi import Climate
from demandlib.vdi.regions import Region


@pytest.fixture
def example_houses():
    return [
        {
            "N_Pers": 3,
            "name": "EFH_1",
            "N_WE": 1,
            "Q_Heiz_a": 6000,
            "house_type": "EFH",
            "Q_TWW_a": 1500,
            "W_a": 5250,
            "summer_temperature_limit": 15,
            "winter_temperature_limit": 5,
        },
        {
            "N_Pers": 45,
            "name": "MFH_1",
            "N_WE": 15,
            "Q_Heiz_a": 60000,
            "house_type": "MFH",
            "Q_TWW_a": 15000,
            "W_a": 45000,
            "summer_temperature_limit": 14,
            "winter_temperature_limit": 4,
        },
    ]


@pytest.fixture
def example_holidays():
    return {
        datetime.date(2017, 1, 1): "New year",
        datetime.date(2017, 12, 25): "Christmas Day",
    }


@pytest.fixture
def example_seasons():
    return {
        "summer1": [5, 15, 9, 14],  # summer: 15.05. to 14.09
        "transition1": [3, 21, 5, 14],  # transition1 :21.03. to 14.05
        "transition2": [9, 15, 10, 31],  # transition2 :15.09. to 31.10
        "winter1": [1, 1, 3, 20],  # winter1:  01.01. to 20.03
        "winter2": [11, 1, 12, 31],  # winter2: 01.11. to 31.12
    }


class TestVDI4655Profiles:
    def test_load_curve_generation(self, example_houses, example_holidays):
        """Test generation of load curves."""
        region = Region(
            2017,
            Climate().from_try_data(4),
            houses=example_houses,
            holidays=example_holidays,
            resample_rule="1h",
        )
        load_curves = region.get_load_curve_houses()

        # Check basic properties of the result
        assert isinstance(load_curves, pd.DataFrame)
        assert not load_curves.empty
        assert "EFH_1" in load_curves.columns.get_level_values(0)
        assert "MFH_1" in load_curves.columns.get_level_values(0)
        # Check sum of the energy values
        assert load_curves.sum().sum() == 132750

    def test_resample_rule(self, example_houses):
        """Test different resample rules."""
        region_hourly = Region(
            2017,
            Climate().from_try_data(4),
            houses=example_houses,
            resample_rule="1h",
        )
        region_quarter = Region(
            2017,
            Climate().from_try_data(4),
            houses=example_houses,
            resample_rule="15min",
        )

        load_curves_hourly = region_hourly.get_load_curve_houses()
        load_curves_quarter = region_quarter.get_load_curve_houses()

        # Quarter-hourly data should have 4 times as many entries
        assert len(load_curves_quarter) == len(load_curves_hourly) * 4

    def test_leap_year(self):
        """Test handling of leap years."""
        # region_leap = Region(2020, try_region=4)  # Leap year
        region_normal = Region(
            2017, Climate().from_try_data(4)
        )  # Non-leap year

        # assert region_leap.hoy == 8784  # Hours in leap year
        assert region_normal.hoy == 8760  # Hours in normal year

    def test_temperature_limits(self, example_houses):
        """Test custom temperature limits."""
        houses = example_houses.copy()
        houses[0]["summer_temperature_limit"] = 18
        houses[0]["winter_temperature_limit"] = 8

        region = Region(2017, Climate().from_try_data(4), houses=houses)
        temperature_limits = region._get_temperature_level_combinations()

        # Should have two different temperature limit combinations
        assert len(temperature_limits) == 2

    def test_custom_seasons(self, example_houses, example_seasons):
        """Test custom seasons."""
        region = Region(
            2017,
            Climate().from_try_data(4),
            houses=example_houses,
            seasons=example_seasons,
        )
        lc = region.get_load_curve_houses()
        assert round(lc["EFH_1", "EFH", "Q_Heiz_TT"].iloc[5000], 5) == 0.03191
        assert region._seasons == example_seasons
        assert region._set_season == "fix"

    def test_zero_summer_heat_demand(self, example_houses):
        """Test zero summer heat demand option."""
        region = Region(
            2017,
            Climate().from_try_data(4),
            houses=example_houses,
            resample_rule="1h",
            zero_summer_heat_demand=True,
        )
        load_curves = region.get_load_curve_houses()

        # Verify that summer heat demand is zero
        # (This would need more specific checks based on actual summer days)
        assert isinstance(load_curves, pd.DataFrame)
        assert not load_curves.empty
        assert (
            load_curves.loc[
                "2017-06-02 12:00", (slice(None), slice(None), "Q_Heiz_TT")
            ].sum()
            == 0
        )

    def test_energy_demand_zero_sum(self, example_houses):
        """Test handling of zero sum energy demands."""
        houses = example_houses.copy()
        houses[0]["Q_Heiz_a"] = 0  # Set heating demand to zero

        region = Region(2017, Climate().from_try_data(4), houses=houses)
        load_curves = region.get_load_curve_houses()

        # Zero annual demand should result in zero load curve
        assert (load_curves.loc[:, ("EFH_1", "EFH", "Q_Heiz_TT")] == 0).all()

    def test_find_try_region(self):
        try_region = demandlib.vdi.find_try_region(13.42, 52.82)
        assert try_region == 4

    def test_negative_factors_warning(self, example_houses):
        """Test warning for negative typical day factors."""
        houses = example_houses.copy()
        houses[0]["N_Pers"] = 999
        houses[0]["N_WE"] = 999

        with pytest.warns(UserWarning, match=".*was negative, see VDI 4655.*"):
            region = Region(2017, Climate().from_try_data(4), houses=houses)
            load_curves = region.get_load_curve_houses()
            assert not load_curves.empty

    def test_dwd_weather_file_missing_header(self):
        """Test error handling for weather file with missing header."""
        import tempfile

        # Create temporary file without proper header
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as tf:
            tf.write("Some data without header\n1 2 3 4 5\n")
            temp_filepath = tf.name

        try:
            with pytest.raises(TypeError, match="Header row not found"):
                from demandlib.vdi.dwd_try import read_dwd_weather_file

                read_dwd_weather_file(weather_file_path=temp_filepath)
        finally:
            os.remove(temp_filepath)

    def test_wrong_house_type(self, example_houses):
        houses = example_houses + [
            {
                "N_Pers": 3,
                "name": "Wrong_heouse_type",
                "N_WE": 1,
                "Q_Heiz_a": 6000,
                "house_type": "wrong",
                "Q_TWW_a": 1500,
                "W_a": 5250,
                "summer_temperature_limit": 15,
                "winter_temperature_limit": 5,
            }
        ]
        with pytest.raises(ValueError, match="The following house"):
            Region(2017, climate=Climate().from_try_data(4), houses=houses)

    def test_house_missing_energy_values(self, example_houses):
        """Test handling of houses with missing energy values."""
        houses = example_houses.copy()
        # Remove some energy values
        del houses[0]["Q_Heiz_a"]
        del houses[0]["W_a"]

        region = Region(
            2017, climate=Climate().from_try_data(4), houses=houses
        )
        with pytest.raises(KeyError, match="Q_Heiz_a"):
            region.get_load_curve_houses()

    def test_invalid_try_region_warning(self, example_houses):
        """Test warning and skipping behavior for invalid TRY region."""
        with pytest.raises(
            ValueError, match="is not a valid number of a DWD TRY region."
        ):
            Region(
                2017,
                Climate().from_try_data(try_region=999),  # Invalid try region
                houses=example_houses,
            )

    def test_dwd_try_missing_geopandas(self, monkeypatch):
        """Test error handling when geopandas is not available."""
        # Mock the imports to raise ImportError
        monkeypatch.setitem(sys.modules, "geopandas", None)

        # Force reload of module to trigger ModuleNotFoundError during imports
        import importlib

        # import demandlib.vdi.dwd_try
        importlib.reload(demandlib.vdi.dwd_try)

        # Should raise a helpful error when trying to use find_try_region
        with pytest.raises(ImportError, match="geopandas.* required.*"):
            demandlib.vdi.dwd_try.find_try_region(13.42, 52.82)

    def test_custom_weather_data(self, example_houses):
        test_path = Path(Path(__file__).parent, "test_data")

        # Einlesen der CSV-Daten
        energy_factors = pd.read_csv(
            Path(test_path, "energy_factors_test.csv"),
            index_col=[0, 1],
            header=[0],
        )

        temperatur_test = pd.read_csv(
            Path(test_path, "temperature_test.csv"), index_col=0
        ).squeeze()

        cloud_coverage_test = pd.read_csv(
            Path(test_path, "cloud_coverage_test.csv"), index_col=0
        ).squeeze()

        custom_climate = Climate(
            temperature=temperatur_test,
            cloud_coverage=cloud_coverage_test,
            energy_factors=energy_factors,
        )

        test_region = Region(
            2017,
            climate=custom_climate,
            resample_rule="1h",
            zero_summer_heat_demand=True,
        )
        test_region.add_houses(example_houses)
        test_region.get_load_curve_houses()
        lc = test_region.get_load_curve_houses().sum()
        assert lc.loc["EFH_1", "EFH", "Q_Heiz_TT"] == 6000.0
        assert lc.loc["MFH_1", "MFH", "Q_Heiz_TT"] == 60000.0
        assert round(lc.loc["EFH_1", "EFH", "Q_TWW_TT"], 10) == 1500.0

    def test_custom_weather_data_wrong_parameter(self, example_houses):
        test_path = Path(Path(__file__).parent, "test_data")

        # Einlesen der CSV-Daten
        energy_factors = pd.read_csv(
            Path(test_path, "energy_factors_test.csv"),
            index_col=[0, 1],
            header=[0],
        )

        temperatur_test = pd.read_csv(
            Path(test_path, "temperature_test.csv"), index_col=0
        ).squeeze()

        my_climate = Climate(
            temperature=temperatur_test,
            cloud_coverage=None,
            energy_factors=energy_factors,
        )

        with pytest.raises(
            AttributeError, match="Climate object not complete."
        ):
            Region(
                2017,
                climate=my_climate,
                resample_rule="1h",
                zero_summer_heat_demand=True,
            )
