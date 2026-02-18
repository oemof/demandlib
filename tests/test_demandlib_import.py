import pytest

import pandas as pd


def test_demandlib_import():
    index15m = pd.date_range(
        start="2020-01-01 00:00",
        end="2020-01-31 23:45",
        freq="15min",
    )

    # To test the imports including warnings, we need to do it at runtime.
    # As the import only happens once,
    # adding more tests might lead to problems.
    with pytest.warns(FutureWarning, match="oemof.demand"):
        import demandlib

    h25_std = demandlib.bdew.H25(index15m)

    assert len(h25_std) == len(index15m)
