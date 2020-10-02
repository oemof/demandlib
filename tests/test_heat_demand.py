from demandlib.examples import heat_demand_example
import os


def test_heat_example():
    """Test the results of the heat example."""
    assert int(heat_demand_example.heat_example(True).sum().sum()) == 245001
