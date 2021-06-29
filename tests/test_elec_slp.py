from demandlib import bdew
import pandas as pd


class TestElecSLP:
    @classmethod
    def setup_class(cls):
        cls.slp = bdew.ElecSlp(2010)

    def test_elec_slp_year(self):
        assert self.slp.year == 2010

    def test_columns_of_frame(self):
        assert sorted(self.slp.slp_frame.columns) == [
            "g0",
            "g1",
            "g2",
            "g3",
            "g4",
            "g5",
            "g6",
            "h0",
            "l0",
            "l1",
            "l2",
        ]

    def test_index_of_frame(self):
        assert isinstance(self.slp.slp_frame.index, pd.DatetimeIndex)
        assert len(self.slp.slp_frame.index) == 35040
        # leap year
        assert len(bdew.ElecSlp(2012).slp_frame.index) == 35040 + 24 * 4
