# -*- coding: utf-8 -*-
"""
Read DWD TRY (test reference year) data.

SPDX-FileCopyrightText: Joris Zimmermann
SPDX-FileCopyrightText: Uwe Krien

SPDX-License-Identifier: MIT
"""

import os

import pandas as pd

try:
    import geopandas as gpd
    from shapely.geometry import Point
except ModuleNotFoundError:
    pass


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
        os.path.dirname(__file__), "resources_weather", "TRY_polygons.geojson"
    )
    try_map = gpd.read_file(fn_try_map)
    my_point = Point(longitude, latitude)
    return int(try_map.loc[try_map.contains(my_point), "TRY_code"])


def read_dwd_weather_file(weather_file_path=None, try_region=None):
    """Read and interpolate 'DWD Testreferenzjahr' files."""
    if weather_file_path is None:
        weather_file_path = os.path.join(
            os.path.dirname(__file__),
            "resources_weather",
            "TRY2010_{:02d}_Jahr.dat".format(try_region),
        )
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
        sep=r'\s+',
        skiprows=header_row - 1,
        index_col=["MM", "DD", "HH"],
        usecols=["MM", "DD", "HH", "t", "N"],
        comment="*",
    )

    # Rename the columns
    weather_data.rename(
        columns={
            "t": "TAMB",
            "N": "CCOVER",
        },
        inplace=True,
    )

    return weather_data
