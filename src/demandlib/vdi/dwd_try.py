# -*- coding: utf-8 -*-
"""
Read DWD TRY (test reference year) data.

SPDX-FileCopyrightText: Joris Zimmermann
SPDX-FileCopyrightText: Uwe Krien

SPDX-License-Identifier: MIT
"""

import pandas as pd
import geopandas as gpd
import os
from shapely.geometry import Point


def find_try_region(longitude, latitude):
    """
    Find the DWD TRY region by coordinates.

    Notes
    -----
    The packages geopandas and shapely need to be installed to use this
    function.

    Parameters
    ----------
    longitude : float
    latitude : float

    Returns
    -------
    DWD TRY region. : int

    """
    fn_try_map = os.path.join(
            os.path.dirname(__file__),
            "resources_weather",
            "TRY_polygons.geojson"
        )
    try_map = gpd.read_file(fn_try_map)
    my_point = Point(longitude, latitude)
    return int(try_map.loc[try_map.contains(my_point), "TRY_code"])


def read_dwd_weather_file(weather_file_path):
    """Read and interpolate "DWD Testreferenzjahr" files."""
    # The comments in DWD files before the header are not commented out.
    # Thus we have to search for the line with the header information:
    header_row = None
    with open(weather_file_path, "r") as rows:
        for number, row in enumerate(rows, 1):
            # The header is the row before the appearance of '***'
            if "***" in row:
                header_row = number - 1
                break

    # Plausibility check:
    if header_row is None:
        msg = (
            "Error: Header row not found in weather file. "
            'Is the data type "DWD" correct? Exiting...\nFile is: '
            + weather_file_path
        )
        raise TypeError(msg)

    # Read the file and store it in a DataFrame
    weather_data = pd.read_csv(
        weather_file_path,
        delim_whitespace=True,
        skiprows=header_row - 1,
        index_col=["MM", "DD", "HH"],
        usecols=["MM", "DD", "HH", "B", "D", "t", "WG", "RF", "WR", "N", "p"],
        comment="*",
    )

    # Rename the columns to the TRNSYS standard:
    weather_data.rename(
        columns={
            "B": "IBEAM_H",
            "D": "IDIFF_H",
            "t": "TAMB",
            "WG": "WSPEED",
            "RF": "RHUM",
            "WR": "WDIR",
            "N": "CCOVER",
            "p": "PAMB",
        },
        inplace=True,
    )

    # Add an 'HOUR' column:
    weather_data["HOUR"] = range(1, 8761)

    return weather_data
